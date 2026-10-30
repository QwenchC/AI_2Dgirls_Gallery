/* Buildless, network-free UI. data/gallery-data.js is generated from reviewed JSON. */
(() => {
  'use strict';
  const data = window.AI_GALLERY;
  if (!data || !Array.isArray(data.characters)) {
    document.getElementById('result-count').textContent = '资料文件未加载，请保持 data 目录与 index.html 一起移动。';
    return;
  }
  const $ = (id) => document.getElementById(id);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const labels = {standard:'标准版',medium:'中间体型版',chibi:'Q 版'};
  const statusLabels = {community:'有社区作品依据',limited:'社区线索 · 证据有限',unverified:'公开设定待核实'};
  let variant = 'standard';
  let selected = null;
  let detailVariant = 'standard';
  let tab = 'profile';
  let lastFocus;
  let toastTimer;
  let briefMeta;
  let briefEdited = false;
  const promptInputs = ['prompt-character','prompt-variant','prompt-scene','prompt-action','prompt-camera'];
  const promptOptions = () => JSON.stringify(promptInputs.map(id => $(id).value));
  const externalURL = (url) => /^https:\/\//i.test(url) ? url : '#';
  const list = (items) => `<ul>${items.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
  const prose = (value) => Array.isArray(value) ? value.join('；') : value;

  function renderGrid() {
    const query = $('search').value.trim().toLocaleLowerCase();
    const results = data.characters.filter(c => [c.name,c.id,...c.aliases,c.visual.label,c.visual.subtitle,c.visual.visual,...c.visual.tags,c.communitySummary,...c.projectSetting.personality].join(' ').toLocaleLowerCase().includes(query));
    $('result-count').textContent = `收录 ${results.length} / ${data.characters.length} 位角色 · 当前展示${labels[variant]}`;
    $('empty-state').hidden = results.length !== 0;
    $('character-grid').innerHTML = results.map(c => `<button class="character-card" data-character="${esc(c.id)}" aria-label="查看 ${esc(c.visual.label)} ${labels[variant]}资料"><span class="card-picture"><img src="${esc(c.images[variant].preview)}" alt="${esc(c.visual.label)}${labels[variant]}多视图参考" width="900" height="675" loading="lazy" decoding="async"></span><span class="card-info"><span class="card-topline"><strong>${esc(c.visual.label)}</strong><span class="card-index">NO. ${String(data.characters.indexOf(c)+1).padStart(2,'0')}</span></span><span class="card-subtitle">${esc(c.visual.subtitle)}</span><span class="card-bottom"><span class="card-tags">${c.visual.tags.map(t=>`<span class="card-tag">${esc(t)}</span>`).join('')}</span><span class="card-arrow" aria-hidden="true">↗</span></span></span></button>`).join('');
  }

  function renderDetailImage() {
    const image = selected.images[detailVariant];
    $('detail-image').src = image.preview;
    $('detail-image').alt = `${selected.visual.label}${labels[detailVariant]}多视图参考`;
    $('original-link').href = image.original;
    $('download-image').href = image.original;
    $('download-image').download = image.original.split('/').pop();
    if (!$('detail-variants').childElementCount) {
      $('detail-variants').innerHTML = Object.entries(labels).map(([key,label])=>`<button data-variant="${key}">${label}</button>`).join('');
    }
    $('detail-variants').querySelectorAll('button').forEach(button => {
      const active = button.dataset.variant === detailVariant;
      button.classList.toggle('active',active);
      button.setAttribute('aria-pressed',String(active));
    });
  }

  function renderDetailContent() {
    const c = selected;
    const p = c.projectSetting;
    $('detail-tabs').querySelectorAll('button').forEach(b => {b.classList.toggle('active',b.dataset.tab===tab);b.setAttribute('aria-selected',String(b.dataset.tab===tab));b.tabIndex=b.dataset.tab===tab?0:-1;});
    $('detail-content').setAttribute('aria-labelledby',`tab-${tab}`);
    if (tab === 'profile') {
      $('detail-content').innerHTML = `<span class="evidence-badge">${esc(statusLabels[c.evidenceStatus])}</span><h3>社区里的她</h3><p>${esc(c.communitySummary)}</p>${c.communityTraits.length ? `<ul>${c.communityTraits.map(t=>`<li>${esc(t.text)} <small>[${esc(t.sourceIds.join('、'))}]</small></li>`).join('')}</ul>` : ''}<h3>本图视觉观察</h3><p class="visual-note">${esc(c.visual.visual)}<br><small>仅描述本仓库标准版可见元素；生成图可能有细节误差，所选原图为准。</small></p><h3>本项目二创设定 <span class="evidence-badge project">创作建议</span></h3><p><strong>${esc(p.role)}</strong> · ${esc(p.background)}</p>${list(p.personality)}<p><strong>表达方式：</strong>${esc(p.speechStyle)}</p><p><strong>互动灵感：</strong>${esc(prose(p.relationships))}</p><p><small>本项目补充的人设、称号和关系均非官方设定，也不声称是全社区共识。</small></p>`;
    } else if (tab === 'creation') {
      $('detail-content').innerHTML = `<span class="evidence-badge project">本项目创作建议</span><h3>先保留她的辨识度</h3><p>${esc(c.visual.visual)}<br><small>以上为标准版视觉观察，细节以当前所选体型原图为准。</small></p><p><strong>视觉母题：</strong>${esc(c.visual.motif)}</p><h3>可以从这些场景开始</h3>${list(p.scenes)}<h3>参考图使用方法</h3><p>当前选择：${labels[detailVariant]}。本仓库图片为多视图设定板，不是单幅场景。可用原设定板并明确各视角属于同一角色；若出现多人或拼版，可另存一张裁出的单视角参考，并保留关键配饰和体型。</p><p>三种体型代表造型比例，不代表年龄。一次镜头只采用一种体型；保持发色、服装、标志饰品一致，不额外定义年龄、身体特征或角色关系。</p><h3>交给 H3 提示词 Skill</h3><p>点击下方“用这个角色创作”，生成中文创作简报。请先整理实际参考素材，再由 Skill 按对应编号转写为英文六段式 Ref2VA 提示词。若需要台词，另行明确原文与说话者。</p>`;
    } else {
      $('detail-content').innerHTML = `<span class="evidence-badge">调研日期 ${esc(data.updated)}</span><p>以下作品用于支持相应社区描述，不能据此认定当前图片直接源自这些作品、已经授权，或作者之间存在合作关系。</p>${c.sources.length ? c.sources.map(s=>`<article class="source-item"><a href="${esc(externalURL(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><small>[${esc(s.id)}] ${esc(s.author||'作者待核实')} · ${esc(s.date||'日期待核实')} · ${s.type==='official'?'官方资料':'社区作品'}</small><p><strong>支持：</strong>${esc(s.evidence)}</p><p><strong>范围：</strong>${esc(s.limits)}</p></article>`).join('') : '<p>暂未找到足以支持人物性格的公开来源。</p>'}<h3>检索与待核实</h3>${list(c.searchNotes)}<h3>图片来源与致谢</h3><p>Creeper-北极之光向维护者提供了初始形象参考图；本仓库图片由维护者使用 GPT 参考其图生成。更上游的参考关系尚未完成考证。侵删；贡献者可联系维护者补充署名与来源。</p><p><small>外部链接需要联网；本页摘要、角色文本与创作指南均已保存于本地。致谢和侵删说明不替代授权。</small></p>`;
    }
  }

  function openCharacter(id) {
    selected = data.characters.find(c => c.id === id);
    if (!selected) return;
    detailVariant = variant;
    tab = 'profile';
    lastFocus = document.activeElement;
    $('dialog-eyebrow').textContent = `CHARACTER / ${selected.id.toUpperCase()}`;
    $('dialog-title').textContent = selected.visual.label;
    $('dialog-subtitle').textContent = selected.visual.subtitle;
    $('character-file').href = `docs/characters/${selected.id}.md`;
    renderDetailImage();renderDetailContent();
    $('character-dialog').showModal();
    document.body.style.overflow = 'hidden';
    $('close-dialog').focus();
  }

  function toast(message) {
    clearTimeout(toastTimer);$('toast').textContent=message;$('toast').classList.add('show');
    toastTimer=setTimeout(()=>$('toast').classList.remove('show'),3000);
  }

  function generatePrompt() {
    const c=data.characters.find(c=>c.id===$('prompt-character').value);
    const type=$('prompt-variant').value;
    briefMeta = {character:c.id, variant:type, label:c.visual.label, options:promptOptions()};
    briefEdited = false;
    $('prompt-text').value = `【AI MUSE · 角色创作简报】\n角色：${c.visual.label}\n体型：${labels[type]}（造型比例，不定义年龄）\n参考图：${c.images[type].original}\n\n【角色一致性】\n${c.visual.visual}\n以上为标准版视觉观察；细节以所选体型的实际参考图为准。保留发色、服装配色与标志饰品，不混用其他体型。\n\n【镜头意图】\n场景：${$('prompt-scene').value.trim()||'由创作者补充'}\n动作与情绪：${$('prompt-action').value.trim()||'由创作者补充'}\n镜头：${$('prompt-camera').value}\n气质参考（本项目二创设定）：${c.projectSetting.personality.join('、')}\n\n【给 H3 提示词 Skill】\n多视图设定板的各视角属于同一角色，不复制拼版与文字。若需要裁出单视角，另存副本并保留关键配饰与体型，不覆盖原图。先确认实际参考图、视频、音频的上传顺序及编号，不从文件名猜测。\n请按 Ref2VA 的 subject_definitions、summary、retention_analysis、detailed_description、overall_soundscape、non_diegetic_music 六段式标记结构转写为提示词；具体格式见本地 Skill 指南。\n叙述使用英文；若需要中文台词，保留台词原文并按官方标签规则标注说话者。当前未指定台词，不擅自添加台词。音效、配乐、时长由创作者确认。\n\n【创作边界】\n不要把角色称号、性格与关系写成官方事实。生成前复核素材授权和上游要求。\n本便笺仅提供文本，不上传参考图、不调用模型、不自动执行生成。`;
  }

  function renderBriefStatus() {
    const stale = briefMeta.options !== promptOptions();
    const text = briefEdited ? '当前文本已手动编辑，下载使用通用文件名。' : `当前简报：${briefMeta.label} · ${labels[briefMeta.variant]}。`;
    $('prompt-status').textContent = text + (stale ? ' 选项已更改，点击“生成创作简报”可更新正文。' : '');
    $('prompt-status').classList.toggle('pending',stale);
  }

  function renderWorkflow() {
    const w=data.workflow;
    $('workflow-summary').textContent=w.summary;
    $('workflow-steps').innerHTML=w.steps.map(s=>`<li><h4>${esc(s.title)}</h4><p>${esc(s.text)}</p></li>`).join('');
    $('workflow-settings').innerHTML=`<table><caption class="sr-only">H3 通用参数指引</caption><thead><tr><th>检查项</th><th>设置思路</th><th>说明</th></tr></thead><tbody>${w.settings.map(s=>`<tr><th>${esc(s.label)}</th><td>${esc(s.value)}</td><td>${esc(s.note)}</td></tr>`).join('')}</tbody></table><h4>六字段格式</h4><p>${w.promptFormat.map(esc).join(' / ')}</p><h4>使用边界</h4>${list(w.limitations)}<p>${w.sources.map(s=>`<a class="text-link" href="${esc(externalURL(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a>`).join('　')}</p>`;
  }

  $('variant-switch').addEventListener('click',e=>{const b=e.target.closest('button[data-variant]');if(!b)return;variant=b.dataset.variant;$('variant-switch').querySelectorAll('button').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b));});renderGrid();});
  $('search').addEventListener('input',renderGrid);
  $('clear-search').addEventListener('click',()=>{$('search').value='';renderGrid();$('search').focus();});
  $('character-grid').addEventListener('click',e=>{const b=e.target.closest('[data-character]');if(b)openCharacter(b.dataset.character);});
  $('hero-open').addEventListener('click',()=>openCharacter('deepseek'));
  $('hero-detail').addEventListener('click',()=>openCharacter('deepseek'));
  $('close-dialog').addEventListener('click',()=>$('character-dialog').close());
  $('character-dialog').addEventListener('close',()=>{document.body.style.overflow='';if(lastFocus?.isConnected)lastFocus.focus({preventScroll:true});});
  $('character-dialog').addEventListener('click',e=>{if(e.target===$('character-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
  $('detail-variants').addEventListener('click',e=>{const b=e.target.closest('[data-variant]');if(!b)return;detailVariant=b.dataset.variant;renderDetailImage();renderDetailContent();});
  $('detail-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-tab]');if(!b)return;tab=b.dataset.tab;renderDetailContent();});
  $('detail-tabs').addEventListener('keydown',e=>{const buttons=[...$('detail-tabs').querySelectorAll('button')];let i=buttons.indexOf(document.activeElement);if(i<0)return;if(e.key==='ArrowRight')i=(i+1)%buttons.length;else if(e.key==='ArrowLeft')i=(i+buttons.length-1)%buttons.length;else if(e.key==='Home')i=0;else if(e.key==='End')i=buttons.length-1;else return;e.preventDefault();tab=buttons[i].dataset.tab;renderDetailContent();buttons[i].focus();});
  $('use-character').addEventListener('click',()=>{$('prompt-character').value=selected.id;$('prompt-variant').value=detailVariant;generatePrompt();renderBriefStatus();lastFocus=$('prompt-scene');$('character-dialog').close();$('studio').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});$('prompt-scene').focus({preventScroll:true});});
  $('prompt-character').innerHTML=data.characters.map(c=>`<option value="${esc(c.id)}">${esc(c.visual.label)}</option>`).join('');
  $('prompt-character').value='deepseek';
  $('generate-prompt').addEventListener('click',()=>{generatePrompt();renderBriefStatus();toast('创作简报已更新');});
  promptInputs.forEach(id => {
    $(id).addEventListener('input',renderBriefStatus);
    $(id).addEventListener('change',renderBriefStatus);
  });
  $('prompt-text').addEventListener('input',()=>{briefEdited=true;renderBriefStatus();});
  $('copy-prompt').addEventListener('click',async()=>{try{if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText($('prompt-text').value);}else{$('prompt-text').focus();$('prompt-text').select();if(!document.execCommand('copy'))throw new Error('copy');}toast('已复制创作简报');}catch{$('prompt-text').focus();$('prompt-text').select();toast('请按 Ctrl+C 或使用下载按钮');}});
  $('download-prompt').addEventListener('click',()=>{const blob=new Blob(['\ufeff'+$('prompt-text').value],{type:'text/plain;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=briefEdited?'AI-MUSE-edited-brief.txt':`AI-MUSE-${briefMeta.character}-${briefMeta.variant}-brief.txt`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);toast('已准备下载创作简报');});
  document.addEventListener('keydown',e=>{if(e.key==='/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName) && !$('character-dialog').open){e.preventDefault();$('search').focus();}});
  renderGrid();renderWorkflow();generatePrompt();renderBriefStatus();
})();
