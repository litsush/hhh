/* Shared drawer pop-up used by index.html (flat wall) and 3d.html. DrawerView.open(drawer, elementToRefocus) */
(function(){
const H=`<section class="open" id="open" role="dialog" aria-modal="true" aria-labelledby="ttl"><div class="inner">
<div class="top"><div><h2 id="ttl"></h2><p id="sub"></p></div><button class="x" id="close">Close</button></div>
<div class="bay" id="bay"><div class="tray" id="tray"></div></div><img class="front" id="front" alt="">
<div class="detail" id="detail"></div></div></section>`;
document.body.insertAdjacentHTML('beforeend',H);
const $=id=>document.getElementById(id);
const money=c=>c==null?'Price not read':c>=100?'$'+(c/100).toFixed(2):c+'\u00a2';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let last,onClose=null;
function open(d,b,closed){last=b;onClose=closed||null;$('ttl').textContent=d.t;$('sub').textContent=d.s+' \u00b7 Column '+d.c+(d.kind==='bins'?', bins under the drawers':', row '+d.r+(d.h?(d.h=='L'?', left half':', right half'):''));const fr=$('front');if(d.f){fr.src=d.f;fr.style.display=''}else{fr.removeAttribute('src');fr.style.display='none'}
 $('bay').classList.toggle('solo',!d.f);
 const t=$('tray');t.innerHTML='';t.className='tray';t.style.backgroundImage='';t.style.aspectRatio='';t.style.width='';t.style.margin='';
 if(d.items.length&&d.i){t.style.backgroundImage='url('+d.i+')';t.style.aspectRatio=d.px[0]+'/'+d.px[1];if(d.px[1]>d.px[0]*1.2){t.style.width='min(100%, calc(78vh * '+(d.px[0]/d.px[1]).toFixed(4)+'))';t.style.margin='0 auto'}
  d.cells.forEach(([k,x0,y0,x1,y1])=>{const it=d.items[k],n=document.createElement('button');n.className='cell';
   n.style.cssText=`left:${x0*100}%;top:${y0*100}%;width:${(x1-x0)*100}%;height:${(y1-y0)*100}%`;
   n.setAttribute('aria-label',it.n+', '+money(it.p));n.innerHTML='<span>'+esc(it.l)+'</span>';n.onclick=()=>pick(it,n,x0,y0,x1-x0,y1-y0,d);t.appendChild(n)});
  $('detail').innerHTML='<p class="hint">Tap a compartment.</p>'}
 else{t.classList.add('blank');t.textContent='Inside not photographed yet';$('detail').innerHTML='<p class="hint">Send a photo of this open drawer and its compartments fill in here.</p>'}
 $('open').classList.remove('on');$('open').style.display='block';$('open').scrollTop=0;void t.offsetWidth;requestAnimationFrame(()=>requestAnimationFrame(()=>$('open').classList.add('on')));$('close').focus()}
function pick(it,n,l,top,w,h,d){document.querySelectorAll('.cell.sel').forEach(e=>e.classList.remove('sel'));n.classList.add('sel');
 const th=`aspect-ratio:${w*d.px[0]}/${h*d.px[1]};background-image:url(${d.i});background-size:${100/w}% ${100/h}%;background-position:${w<1?l/(1-w)*100:0}% ${h<1?top/(1-h)*100:0}%`;
 const u=it.u?it.u[0]+' '+it.u.slice(1,6)+' '+it.u.slice(6,11)+' '+it.u[11]:'';
 $('detail').innerHTML=`<div class="thumb" style="${th}"></div><div><h3>${esc(it.n)}</h3><div class="price">${money(it.p)}<small> each</small></div><dl><dt>Where</dt><dd>${esc(it.w)}</dd>${it.bq?`<dt>Box</dt><dd>${money(it.bp)} for ${it.bq}</dd>`:''}<dt>${it.u?'SKU':'Label no.'}</dt><dd>${esc(it.k)||'—'}</dd>${u?`<dt>UPC</dt><dd>${u}</dd>`:''}</dl>${it.x?'<p class="nt">'+esc(it.x)+'</p>':''}</div>`}
function shut(){$('open').classList.remove('on');$('open').style.display='';if(last&&last.focus)last.focus();const f=onClose;onClose=null;if(f)f()}
const isOpen=()=>$('open').classList.contains('on')||$('open').style.display==='block';
$('close').onclick=shut;addEventListener('keydown',e=>{if(e.key==='Escape'&&isOpen())shut()});
window.DrawerView={open,shut,isOpen};
})();
