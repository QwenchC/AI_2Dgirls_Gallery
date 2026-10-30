import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8').replace(/^\uFEFF/,'');
const json=p=>JSON.parse(read(p));
const failures=[];
let checks=0;
function check(condition,message){checks++;if(!condition)failures.push(message);}
const exists=p=>fs.existsSync(path.resolve(root,p));
const data=json('data/gallery-data.json');
const manifest=json('data/original-images.json');
const sandbox={window:{}};
vm.runInNewContext(read('data/gallery-data.js'),sandbox);
check(JSON.stringify(sandbox.window.AI_GALLERY)===JSON.stringify(data),'Script and JSON data differ');
check(data.characters.length===14,'Expected 14 characters');
check(new Set(data.characters.map(c=>c.id)).size===14,'Character ids must be unique');
check(manifest.files.length===42,'Expected 42 originals');
for(const f of manifest.files){
  check(exists(f.path),`Missing original: ${f.path}`);
  if(exists(f.path)){
    const buffer=fs.readFileSync(path.join(root,f.path));
    check(buffer.length===f.bytes,`Original size changed: ${f.path}`);
    check(crypto.createHash('sha256').update(buffer).digest('hex')===f.sha256,`Original hash changed: ${f.path}`);
  }
}
for(const c of data.characters){
  check(['community','limited','unverified'].includes(c.evidenceStatus),`Invalid evidence status: ${c.id}`);
  check(exists(`docs/characters/${c.id}.md`),`Missing dossier: ${c.id}`);
  const ids=new Set(c.sources.map(s=>s.id));
  check(ids.size===c.sources.length,`Duplicate source id within ${c.id}`);
  for(const trait of c.communityTraits)for(const id of trait.sourceIds)check(ids.has(id),`Unresolved source ${id} in ${c.id}`);
  for(const source of c.sources){
    check(/^https:\/\//.test(source.url),`Non-HTTPS external source in ${c.id}`);
    check(Boolean(source.evidence&&source.limits&&source.accessed),`Incomplete source scope in ${c.id}`);
  }
  for(const variant of ['standard','medium','chibi']){
    check(exists(c.images[variant].original),`Missing ${c.id}/${variant} original`);
    check(exists(c.images[variant].preview),`Missing ${c.id}/${variant} preview`);
    check(manifest.files.some(f=>f.path===c.images[variant].original),`Untracked original in ${c.id}/${variant}`);
  }
  check(c.projectSetting.personality.length>0&&c.projectSetting.scenes.length>0,`Incomplete setting in ${c.id}`);
}
const html=read('index.html');
for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g)){
  const url=match[1];
  if(url.startsWith('#'))continue;
  check(!/^(?:https?:)?\/\//.test(url),`Unexpected external initial HTML dependency: ${url}`);
  check(exists(decodeURIComponent(url.split('#')[0])),`Missing HTML resource: ${url}`);
}
const code=read('assets/app.js');
check(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(code),'Unexpected runtime network API');
check(!/@import|url\(\s*['"]?https?:/i.test(read('assets/style.css')),'Unexpected CSS network dependency');
check(!code.includes('六字段 JSON'),'Incorrect Ref2VA JSON instruction');
check(read('README.md').includes('Creeper-北极之光')&&read('README.md').includes('侵删'),'Missing required attribution');
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).filter(e=>!['.git','artifacts','node_modules'].includes(e.name)).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
for(const file of walk(root).filter(f=>f.endsWith('.md'))){
  const content=fs.readFileSync(file,'utf8');
  for(const m of content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
    const link=m[1];
    if(/^(?:[a-z]+:|#)/i.test(link))continue;
    // This report is written at the end of this invocation.
    if(path.resolve(path.dirname(file),link)===path.join(root,'artifacts','verification.json'))continue;
    check(fs.existsSync(path.resolve(path.dirname(file),decodeURIComponent(link.split('#')[0]))),`Broken Markdown link in ${path.relative(root,file)}: ${link}`);
  }
}
const report={date:'2026-10-30',checks,passed:checks-failures.length,failures,originalsVerified:manifest.files.length,characters:data.characters.length,sourceReferences:data.characters.reduce((n,c)=>n+c.sources.length,0),uniqueSourceURLs:new Set(data.characters.flatMap(c=>c.sources.map(s=>s.url))).size,scope:'Static consistency, local links, no initial remote dependencies, preservation hashes. Does not claim browser or model inference acceptance.'};
if(process.argv.includes('--write-report')){
  fs.mkdirSync(path.join(root,'artifacts'),{recursive:true});
  fs.writeFileSync(path.join(root,'artifacts','verification.json'),JSON.stringify(report,null,2)+'\n');
}
console.log(JSON.stringify(report,null,2));
if(failures.length)process.exitCode=1;
