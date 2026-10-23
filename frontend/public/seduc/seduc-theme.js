(function(){
var V='37';
function fontsLink(){
 if(document.getElementById('ceb-fonts'))return;
 var l=document.createElement('link');l.id='ceb-fonts';l.rel='stylesheet';l.href='/idcap/fonts.css?v='+V;document.head.appendChild(l);
 var f=document.createElement('link');f.id='idcap-flow';f.rel='stylesheet';f.href='/idcap/flow.css?v='+V;document.head.appendChild(f);
}
function host(id,html,cls,atTop){
 var h=document.createElement('div');h.id=id;
 h.style.cssText='display:block;width:100%;position:relative;z-index:'+(atTop?'9999':'100')+';visibility:hidden;';
 if(atTop)document.body.insertBefore(h,document.body.firstChild);else document.body.appendChild(h);
 var r=h.attachShadow({mode:'open'});
 r.innerHTML='<link rel="stylesheet" href="/idcap/chrome.css?v='+V+'"><div class="sfbody '+cls+'">'+html+'</div>';
 var ln=r.querySelector('link');
 function show(){h.style.visibility='visible';if(atTop){var done=function(){document.documentElement.classList.remove('vn-wait');};var fr=document.fonts&&document.fonts.ready;if(fr){Promise.race([fr,new Promise(function(r){setTimeout(r,1200);})]).then(done);}else done();}}
 ln.addEventListener('load',show);
 ln.addEventListener('error',function(){h.remove();document.documentElement.classList.remove('vn-wait');});
 setTimeout(show,2500);
 r.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a');if(!a)return;
  var hr=a.getAttribute('href');
  if(!hr||hr==='#'){e.preventDefault();return;}
  var pl=document.getElementById('__page_loader');if(pl)pl.classList.remove('__hidden');
 });
 return r;
}
function menu(r){
 var ib=r.getElementById('idcap-menu-btn');
 if(ib){var w=r.querySelector('.sfbody'),tg=r.querySelector('.header__toggle');function st(on){w.classList.toggle('menu-on',on);document.documentElement.style.overflow=on?'hidden':'';}ib.addEventListener('click',function(){st(!w.classList.contains('menu-on'));});if(tg)tg.addEventListener('click',function(e){if(e.target===tg)st(false);});document.addEventListener('keydown',function(e){if(e.key==='Escape')st(false);});return;}
 var wrap=r.querySelector('.sfbody'),dr=r.getElementById('mnav'),op=r.getElementById('mnav-open');
 if(!wrap||!dr||!op)return;
 // drawer fora do .sfbody (que recebe transform:scale em telas HiDPI e prenderia o position:fixed)
 var bd=r.getElementById('mnav-backdrop'),layer=document.createElement('div');
 layer.className='mnav-layer';
 if(bd)layer.appendChild(bd);
 layer.appendChild(dr);
 r.appendChild(layer);
 if(/(pagamento-pix|inscricao-realizada)/.test(location.pathname)){
  dr.querySelectorAll('ul').forEach(function(u){u.remove();});
  dr.querySelectorAll('.mnav-cta a').forEach(function(a){if(!/acompanhamento/i.test(a.textContent))a.remove();});
 }
 var ls=document.createElement('style');
 ls.textContent='.mnav-layer.mnav-on #mnav{transform:none;visibility:visible;box-shadow:-8px 0 30px rgba(0,0,0,.15)}.mnav-layer.mnav-on #mnav-backdrop{opacity:1;pointer-events:auto}';
 r.appendChild(ls);
 function set(on){wrap.classList.toggle('mnav-on',on);layer.classList.toggle('mnav-on',on);dr.setAttribute('aria-hidden',on?'false':'true');document.documentElement.style.overflow=on?'hidden':'';}
 op.addEventListener('click',function(){set(true);});
 r.querySelector('#mnav .mnav-close').addEventListener('click',function(){set(false);});
 r.getElementById('mnav-backdrop').addEventListener('click',function(){set(false);});
 document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false);});
}
function build(p){
 if(document.getElementById('seduc-header-host'))return;
 fontsLink();
 var hr=host('seduc-header-host',p.h,p.cls,true);
 (function(){var hh=document.getElementById('seduc-header-host');function pad(){hh.style.setProperty('position','fixed','important');hh.style.setProperty('top','0','important');hh.style.setProperty('left','0','important');hh.style.setProperty('right','0','important');hh.style.setProperty('z-index','9990','important');document.body.style.setProperty('padding-top',hh.offsetHeight+'px','important');}pad();window.addEventListener('resize',pad);setTimeout(pad,400);})();
 if(/minhas-inscricoes/.test(location.pathname)){hr.querySelectorAll('.header__action-follow-button,[data-testid=header-minhas-inscricoes-btn]').forEach(function(el){el.remove();});}
 menu(hr);
 if(/minhas-inscricoes/.test(location.pathname)){
  hr.querySelectorAll('#mnav-open,.mnav-layer,#idcap-menu-btn').forEach(function(el){el.remove();});
  hr.querySelectorAll('a').forEach(function(a){a.removeAttribute('href');a.style.cursor='default';});
  hr.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();},true);
 }
 document.querySelectorAll('#aocp-footer,.seduc-footer').forEach(function(el){el.remove();});
 host('vunesp-footer-host',p.f,p.cls,false);
}
function go(){
 fetch('/idcap/parts.json?v='+V).then(function(r){return r.json();}).then(build).catch(function(){document.documentElement.classList.remove('vn-wait');});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
