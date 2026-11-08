'use strict';
const $ = (selector) => document.querySelector(selector);
const SOURCE = 'https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab';
let GROUPS = {};

function renderBenchmark(key) {
  const group = GROUPS[key];
  if (!group) return;
  $('[id="chart-title"]').textContent = group.title;
  $('#chart-unit').textContent = group.unit;
  $('#population').textContent = group.population;
  $('#benchmark-verdict').textContent = group.verdict;
  $('#benchmark-explanation').textContent = group.explanation;
  $('#benchmark-panel').setAttribute('aria-labelledby', `tab-${key}`);
  $('#benchmark-bars').replaceChildren(...group.rows.map(([name,value,control]) => {
    const row = document.createElement('div'); row.className = 'benchmark-row';
    const label = document.createElement('span'); label.textContent = name;
    if(control){const mark=document.createElement('small');mark.className='control-mark';mark.textContent='CONTROL';label.append(mark);}
    const track=document.createElement('div');track.className='bar-track';track.setAttribute('aria-hidden','true');
    const bar=document.createElement('div');bar.className='bar';bar.style.width=`${value/group.max*100}%`;track.append(bar);
    const number=document.createElement('b');number.textContent=value.toFixed(2)+(key==='direction'?'%':'');row.append(label,track,number);return row;
  }));
  $('#benchmark-axis').replaceChildren(...group.ticks.map(t=>{const span=document.createElement('span');span.textContent=t;return span;}));
  document.querySelectorAll('[role=tab]').forEach(tab=>{const active=tab.dataset.group===key;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;});
}
document.querySelectorAll('[role=tab]').forEach((tab,index,tabs)=>{
  tab.addEventListener('click',()=>renderBenchmark(tab.dataset.group));
  tab.addEventListener('keydown',event=>{let next;if(event.key==='ArrowRight')next=(index+1)%tabs.length;if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;if(next!==undefined){event.preventDefault();tabs[next].focus();renderBenchmark(tabs[next].dataset.group);}});
});
fetch('data/benchmarks.json').then(response => { if (!response.ok) throw new Error('Benchmark data unavailable'); return response.json(); }).then(groups => { GROUPS = groups; renderBenchmark('direction'); }).catch(error => { $('#benchmark-panel').textContent = 'Benchmark data could not load. Reload or inspect the source protocol on GitHub.'; console.error(error); });
// Decorative bars illustrate a below-threshold region, never a claimed time series.
const heights=[30,36,41,33,43,38,49,40,35,45,52,42,54,48,35,46,51,39,47,55,49,46,38,43,52,48,54,44,56,49,45,52];
$('.chart-bars').replaceChildren(...heights.map(height=>{const i=document.createElement('i');i.style.height=`${height}px`;return i;}));
const STATUS_LABELS={TRAINED_VERIFIED:'TRAINED · VERIFIED',IMPLEMENTED_VERIFIED:'IMPLEMENTED · VERIFIED',TRAINED_REPORTED_ONLY:'REPORTED ONLY',REGISTERED_SEALED:'REGISTERED · SEALED',REJECTED:'REJECTED',INSUFFICIENT_EVIDENCE:'INSUFFICIENT EVIDENCE',EXPERIMENTAL:'EXPERIMENTAL'};
function statusClass(status){return status.includes('SEALED')||status.includes('FROZEN')?'sealed':status==='REJECTED'||status.includes('NEGATIVE')?'rejected':status.includes('VERIFIED')?'verified':'unverified';}
let models=[];
function filteredModels(){const query=$('#model-search').value.trim().toLowerCase();const status=$('#status-filter').value;return models.filter(model=>(status==='all'||model.status===status)&&JSON.stringify(model).toLowerCase().includes(query));}
function inspectModel(model){
  $('#detail-title').textContent=model.id;$('#detail-family').textContent=model.family;$('#detail-status').textContent=STATUS_LABELS[model.status]||model.status;
  $('#detail-fields').replaceChildren(...Object.entries(model).filter(([key])=>!['id','family','status'].includes(key)).flatMap(([key,value])=>{const dt=document.createElement('dt');dt.textContent=key.replaceAll('_',' ');const dd=document.createElement('dd');dd.textContent=value===null?'Not provided':value;return[dt,dd];}));
  $('#model-dialog').showModal();
}
function renderModels(){
  const filtered=filteredModels();
  $('#model-rows').replaceChildren(...filtered.map(model=>{const tr=document.createElement('tr');const name=document.createElement('td');const strong=document.createElement('strong');strong.textContent=model.id;const small=document.createElement('small');small.textContent=model.family;name.append(strong,small);const project=document.createElement('td');project.textContent=model.project||'Historical lineage';const status=document.createElement('td');const badge=document.createElement('span');badge.className=`status ${statusClass(model.status)}`;badge.textContent=STATUS_LABELS[model.status]||model.status;status.append(badge);const action=document.createElement('td');const button=document.createElement('button');button.className='inspect-button';button.textContent='↗';button.setAttribute('aria-label',`Inspect ${model.id}`);button.addEventListener('click',()=>inspectModel(model));action.append(button);tr.append(name,project,status,action);return tr;}));
  if(!filtered.length){const tr=document.createElement('tr');const td=document.createElement('td');td.colSpan=4;td.textContent='No models match these filters. Try another search or evidence status.';tr.append(td);$('#model-rows').append(tr);}
  $('#result-count').textContent=`${filtered.length} of ${models.length} registry entries`;
}
$('#model-search').addEventListener('input',renderModels);$('#status-filter').addEventListener('change',renderModels);
document.addEventListener('keydown',event=>{if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!$('#model-dialog').open){event.preventDefault();$('#model-search').focus();}});
$('#close-dialog').addEventListener('click',()=>$('#model-dialog').close());
$('#model-dialog').addEventListener('click',event=>{if(event.target===$('#model-dialog')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();}});
$('#export-models').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(filteredModels(),null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='gambler-model-registry.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
async function loadRegistry(){try{const results=await Promise.all(['models','experiments'].map(async name=>{const r=await fetch(`data/${name}.json`);if(!r.ok)throw new Error(`Registry request failed: ${r.status}`);return r.json();}));models=results[0];const experiments=results[1];$('#model-count').textContent=models.length;$('#experiment-count').textContent=experiments.length;renderModels();$('#experiment-list').replaceChildren(...experiments.map(experiment=>{const card=document.createElement('article');card.className='experiment-card';const top=document.createElement('div');const id=document.createElement('span');id.textContent=experiment.id;const date=document.createElement('span');date.textContent=experiment.when;top.append(id,date);const title=document.createElement('h3');title.textContent=experiment.what;const result=document.createElement('p');result.className='result';result.textContent=experiment.result||experiment.why_failed||experiment.note||`Earliest review: ${experiment.earliest_review}. Prospective protocol; no result claimed.`;const status=document.createElement('span');status.className=`status ${statusClass(experiment.status)}`;status.textContent=experiment.status.replaceAll('_',' ');card.append(top,title,result,status);return card;}));}catch(error){$('#load-error').hidden=false;$('#load-error').textContent='The research registry could not load. Reload the page or open the source registry on GitHub.';$('#result-count').textContent='Registry unavailable';console.error(error);}}
loadRegistry();
// Mid-quoted spread s implies bid/ask = (1-s/20000)/(1+s/20000).
// The fixture's quote-currency fees compound on each leg: proceeds/N = bid/ask * (1-f)^2.
const FIXTURE_SPREAD=(20438907946-20400971155)/((20438907946+20400971155)/2)*10000;
function renderCost(){const spread=Number($('#spread').value),fee=Number($('#fee').value);const ratio=(1-spread/20000)/(1+spread/20000);const spreadCost=(1-ratio)*10000;const total=(1-ratio*(1-fee/10000)**2)*10000;const feeCost=total-spreadCost;$('#spread-value').textContent=`${spread.toFixed(2)} bps`;$('#fee-value').textContent=`${fee.toFixed(1)} bps`;$('#cost-total').textContent=total.toFixed(2);$('#spread-contribution').textContent=spreadCost.toFixed(2);$('#fee-contribution').textContent=feeCost.toFixed(2);$('#spread-segment').style.width=`${total?spreadCost/total*100:0}%`;$('#fee-segment').style.width=`${total?feeCost/total*100:0}%`;$('#cost-loss').textContent=`−${Math.round(1500000*total/10000).toLocaleString('en-US')} TMN`;
}
function resetCost(){$('#spread').step='any';$('#spread').value=FIXTURE_SPREAD;$('#fee').value=30;renderCost();}
$('#spread').addEventListener('input',renderCost);$('#fee').addEventListener('input',renderCost);$('#reset-cost').addEventListener('click',resetCost);resetCost();
$('#copy-code').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#quickstart').textContent);$('#copy-code').textContent='Copied ✓';}catch{$('#copy-code').textContent='Select commands to copy';const selection=window.getSelection();const range=document.createRange();range.selectNodeContents($('#quickstart'));selection.removeAllRanges();selection.addRange(range);}setTimeout(()=>$('#copy-code').textContent='Copy commands ⧉',2500);});
