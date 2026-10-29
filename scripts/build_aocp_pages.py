import re

SRC = '/app/scripts/aocp_src/'
OUT = '/app/frontend/public/'

EXTRA = '''<style>
html,body{overflow-x:hidden}
@media (max-width:1023px){
 .top-bar{display:flex!important;justify-content:center}
 .top-bar .navbar-center,.top-bar .navbar-end{display:none!important}
 .top-bar .navbar-start{width:auto}
 .top-bar img{width:190px!important;height:auto!important}
 header nav.navbar{padding:.6rem 1rem!important}
 .pt-20{padding-top:4.5rem}
 .pt-20 .text-3xl{font-size:1.45rem;line-height:1.3;padding:1.75rem 1rem}
 .concurso-card h1{font-size:1.05rem}
 footer.footer{padding:1.75rem 1.25rem!important}
}
.linha-inscricao{color:#2f8f6c;display:flex;align-items:center;gap:.45rem}
.linha-inscricao:before{content:'';width:.55rem;height:.55rem;border-radius:50%;background:#38a880;box-shadow:0 0 0 3px rgba(56,168,128,.25);flex-shrink:0}
.btn-inscreva{min-width:220px;height:3.4rem;font-size:1.15rem;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;box-shadow:0 10px 24px -10px rgba(54,169,128,.8);transition:transform .2s,box-shadow .2s}
.btn-inscreva:hover{transform:translateY(-2px);box-shadow:0 14px 28px -10px rgba(54,169,128,.9)}
@media (max-width:639px){
 footer.footer{grid-template-columns:1fr!important;grid-auto-flow:row!important}
 .pagina-concurso{display:grid!important;grid-template-columns:1fr!important}
 .pagina-concurso>.m-3{margin:.5rem 1rem}
 .pagina-concurso h1.pb-10{padding-bottom:1rem;padding-top:1rem}
 .pagina-concurso .p-5{padding:1rem;font-size:.92rem}
}
</style>
<script>
(function(){
 try{var v=localStorage.getItem('visitor_id');if(!v){v='v_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);localStorage.setItem('visitor_id',v);}
 fetch('/api/track/access',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({page:location.pathname,user_agent:navigator.userAgent,extra:{visitor_id:v}})}).catch(function(){});}catch(e){}
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href="#"]');if(a)e.preventDefault();});
})();
</script>
'''


def clean(h):
    h = re.sub(r'<script\b.*?</script>', '', h, flags=re.S)
    h = re.sub(r'<!--.*?-->', '', h, count=1, flags=re.S)
    h = re.sub(r'<meta http-equiv=content-security-policy[^>]*>', '', h)
    h = re.sub(r'<link rel=canonical[^>]*>', '', h)
    h = re.sub(r'<div class="md-chat-widget-wrapper.*$', '', h, flags=re.S)
    h = re.sub(r'<div id=vlibras-access-wrapper>.*?</template></div>', '', h, flags=re.S)
    h = re.sub(r'<next-route-announcer.*?</next-route-announcer>', '', h, flags=re.S)
    h = re.sub(r'<div vw=true.*?<div class=vw-plugin-top-wrapper></div></div></div>', '', h, flags=re.S)
    h = re.sub(r'<button type=button aria-expanded=false aria-label="Abrir o painel de acessibilidade".*?</button>', '', h, flags=re.S)
    h = re.sub(r'<div class="fixed z-\[1000001\].*?</button></div>', '', h, flags=re.S)
    h = re.sub(r'<button type=button class="link-hover link text-left">Preferências de cookies</button>', '', h)
    h = re.sub(r'<div class="w-full justify-between lg:hidden sf-hidden">.*?</ul></div></div></div>', '', h, flags=re.S)
    h = re.sub(r'<div class="flex items-center justify-start"><a class="font-lg text-sm uppercase text-blue-900".*?Voltar</a></div>', '', h, flags=re.S)
    h = h.replace('<div class="mx-auto hidden w-full justify-between lg:flex">', '<div class="mx-auto hidden w-full justify-between lg:flex top-bar">')
    return h


def finish(h, name):
    h = re.sub(r'href=https://www\.institutoaocp\.org\.br/(?=[ >])', 'href=/inicio.html', h)
    h = re.sub(r'href=https://www\.institutoaocp\.org\.br/concursos/status/inscricoes-abertas', 'href=/inicio.html', h)
    h = re.sub(r'href="?https?://[^ >"]+"?', 'href=#', h)
    h = h.replace(' target=_blank', '')
    h = h.rstrip() + '\n' + EXTRA
    open(OUT + name, 'w', encoding='utf-8').write(h)
    left = re.findall(r'https?://(?!www\.w3\.org)[^ >"\')]+', re.sub(r'data:[^"\')]+', '', h))
    print(name, len(h), 'external left:', left[:10])


def build_inicio():
    h = clean(open(SRC + 'inicio_src.html', encoding='utf-8').read())
    h = re.sub(r'<div class="mx-5 mb-10 flex items-center rounded-xl border-2 border-blue-900 p-2"><input[^>]*></div>', '<div class=mb-4></div>', h)
    h = h.replace('>Concursos com Inscrições Abertas</h1>', '>Concursos com Inscrições Abertas em Pernambuco</h1>')
    cards = '''<div class="flex min-w-full flex-col divide-gray-200 overflow-hidden px-5 pb-12 align-middle" id=lista-concursos><div class="my-2 rounded-xl bg-gray-100 p-5 font-medium text-gray-800 concurso-card" data-testid=concurso-pmpe><a href=/pmpe.html><h1 class="text-xl text-gray-800 hover:underline">PMPE - POLÍCIA MILITAR DE PERNAMBUCO</h1><p class="pt-2 font-sans text-sm font-normal hover:underline">Concurso Público nº 001/2026 - Polícia Militar de Pernambuco (PMPE) - Divulgado o Edital de Deferimento e Indeferimento das Solicitações de Isenção da Taxa de Inscrição.</p><p class="pt-2 font-sans text-sm font-semibold linha-inscricao" data-testid=inscricao-data-pmpe>Inscrições abertas até 05/11/2026 às 23h59</p></a></div><div class="my-2 rounded-xl bg-gray-100 p-5 font-medium text-gray-800 concurso-card" data-testid=concurso-cbmpe><a href=/cbmpe.html><h1 class="text-xl text-gray-800 hover:underline">CBMPE - CORPO DE BOMBEIROS MILITAR DE PERNAMBUCO</h1><p class="pt-2 font-sans text-sm font-normal hover:underline">Concurso Público nº 002/2026 - Corpo de Bombeiros Militar de Pernambuco (CBMPE) - Divulgado o Edital de Deferimento e Indeferimento das Solicitações de Isenção da Taxa de Inscrição.</p><p class="pt-2 font-sans text-sm font-semibold linha-inscricao" data-testid=inscricao-data-cbmpe>Inscrições abertas até 05/11/2026 às 23h59</p></a></div></div>'''
    h = re.sub(r'<div class="flex min-w-full flex-col divide-gray-200 overflow-hidden px-5 pb-12 align-middle">.*?</a></div></div>', cards, h, count=1, flags=re.S)
    finish(h, 'inicio.html')


def build_concurso(slug, c, form_id, consulta_id, title):
    h = clean(open(SRC + slug + '_src.html', encoding='utf-8').read())
    h = h.replace('<div class="hidden grid-cols-1 sm:grid sm:grid-cols-2">', '<div class="hidden grid-cols-1 sm:grid sm:grid-cols-2 pagina-concurso" data-testid=' + slug + '-conteudo>')
    h = h.replace('<div class="sm:hidden w-full px-2 sm:px-0 sf-hidden"></div>', '')
    h = re.sub(r'href="https://link\.institutoaocp\.org\.br/open-link\?identificador=' + form_id + r'[^"]*"', 'href=/termos.html?c=' + c + ' data-testid=' + slug + '-link-inscricao', h)
    h = re.sub(r'href="https://link\.institutoaocp\.org\.br/open-link\?identificador=' + consulta_id + r'[^"]*"', 'href=/minhas-inscricoes.html data-testid=' + slug + '-link-consultar', h)
    h = re.sub(r'(<div class="m-3 flex items-center justify-center pb-12 text-justify sm:m-12 sm:text-center"><h2>.*?</h2></div>)', lambda m: m.group(1).replace('pb-12', 'pb-4') + '<div class="flex justify-center pb-12"><a href=/termos.html?c=' + c + ' class="btn-primary btn btn-inscreva text-white" data-testid=' + slug + '-btn-inscreva-se>Inscreva-se</a></div>', h, count=1, flags=re.S)
    h = h.replace('<title>Instituto AOCP - Concursos Públicos</title>', '<title>' + title + ' | Instituto AOCP</title>', 1)
    finish(h, slug + '.html')


TERMOS_MAIN = '''<div class="pt-20 termos-wrap"><main class=termos-sec data-testid=termos-page>
<div class=termos-titulo><h1 class=termos-h1>Termos de Inscrição</h1><span class=termos-bar></span></div>
<article class=termos-card data-testid=termos-card>
<div class=termos-head><img id=t-logo class=termos-logo alt="" data-testid=termos-logo>
<div><span class=termos-tag id=t-edital></span><h2 class=termos-org id=t-orgao data-testid=termos-orgao></h2><p class=termos-desc-org id=t-desc></p></div></div>
<ul class=termos-info>
<li><span>Inscrições até</span><strong>05/11/2026 às 23h59</strong></li>
<li><span>Vagas</span><strong id=t-vagas></strong></li>
<li><span>Regime</span><strong>Estatutário</strong></li>
<li><span>Organizadora</span><strong>Instituto AOCP</strong></li>
</ul>
<div class=termos-body>
<p class=termos-lead>Antes de prosseguir, leia com atenção as condições abaixo:</p>
<ol class=termos-lista>
<li>Li o Edital de Abertura e seus anexos e conheço todas as regras do concurso.</li>
<li>Atendo a todos os requisitos exigidos para o cargo que vou escolher.</li>
<li>As informações que vou fornecer são verdadeiras e de minha inteira responsabilidade.</li>
<li>A inscrição só será efetivada após a confirmação do pagamento da taxa de inscrição.</li>
</ol>
<label class=termos-aceite data-testid=termos-aceite-label><input id=termos name=aceito_termos data-testid=termos-checkbox type=checkbox value=1><span>Declaro que li e concordo com os termos do <b id=t-edital2></b> e seus anexos.</span></label>
<div class=termos-acoes><a href=/inscricao.html id=bt-continuar data-testid=btn-continuar-termos class="btn-primary btn termos-btn text-white" aria-disabled=true>Continuar</a><a href=/inicio.html id=btn-voltar-termos data-testid=btn-voltar-termos class="btn termos-btn termos-btn-out">Voltar</a></div>
</div></article></main></div>
<div id=home-loader aria-hidden=true data-testid=home-loader><div class=spin></div></div>
<style>
.termos-wrap{background:#f6f8fa}
.termos-sec{max-width:980px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
.termos-titulo{text-align:center;margin-bottom:2rem}
.termos-h1{font-size:2rem;text-transform:uppercase;color:#1e3a8a;margin:0}
.termos-bar{display:block;width:2.5rem;height:.25rem;background:#38a880;margin:.5rem auto 0}
.termos-card{background:#fff;border-radius:1rem;box-shadow:0 20px 50px -25px rgba(15,40,90,.35);overflow:hidden;animation:tUp .5s ease both}
@keyframes tUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.termos-head{display:flex;gap:1.5rem;align-items:center;padding:2rem 2.25rem;border-bottom:1px solid #eef0f3;background:linear-gradient(90deg,#f3f4f6,#fff)}
.termos-logo{width:96px;height:96px;object-fit:contain;flex-shrink:0;border-radius:.75rem;background:#fff;padding:.4rem;box-shadow:0 6px 18px -8px rgba(0,0,0,.25)}
.termos-tag{display:inline-block;background:#38a880;color:#fff;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;padding:.2rem .7rem;border-radius:999px}
.termos-org{font-size:1.6rem;color:#1e3a8a;margin:.5rem 0 .25rem;line-height:1.2;font-weight:700}
.termos-desc-org{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:#4b5563;margin:0}
.termos-info{list-style:none;margin:0;padding:1.5rem 2.25rem;display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;border-bottom:1px solid #eef0f3}
.termos-info li{border-left:3px solid #38a880;padding-left:.75rem}
.termos-info span{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:#6b7280}
.termos-info strong{display:block;font-size:1.05rem;color:#111827;line-height:1.3}
.termos-body{padding:1.75rem 2.25rem 2.25rem}
.termos-lead{font-size:1.1rem;color:#1f2937;margin:0 0 1rem}
.termos-lista{counter-reset:t;list-style:none;margin:0 0 1.5rem;padding:0;font-family:ui-sans-serif,system-ui,sans-serif}
.termos-lista li{counter-increment:t;position:relative;padding:.7rem .9rem .7rem 3rem;margin-bottom:.5rem;background:#f9fafb;border-radius:.6rem;color:#374151;font-size:.95rem}
.termos-lista li:before{content:counter(t);position:absolute;left:.85rem;top:50%;transform:translateY(-50%);width:1.5rem;height:1.5rem;border-radius:50%;background:#1e3a8a;color:#fff;font-size:.8rem;display:flex;align-items:center;justify-content:center}
.termos-aceite{display:flex;gap:.85rem;align-items:flex-start;cursor:pointer;padding:.25rem 0;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.95rem;color:#1f2937}
.termos-aceite input{width:1.25rem;height:1.25rem;margin-top:.1rem;accent-color:#38a880;flex-shrink:0}
.termos-acoes{display:flex;gap:.75rem;margin-top:1.75rem}
.termos-btn{min-width:170px;border-radius:999px;font-size:1rem;letter-spacing:.05em;text-transform:uppercase;transition:opacity .2s,transform .2s}
.termos-btn:hover{transform:translateY(-1px)}
.termos-btn-out{background:#fff;border:2px solid #1e3a8a;color:#1e3a8a}
.termos-btn-out:hover{background:#1e3a8a;color:#fff}
#home-loader{position:fixed;inset:0;background:rgba(255,255,255,.9);z-index:9999;display:none;align-items:center;justify-content:center}
#home-loader.on{display:flex}
#home-loader .spin{width:48px;height:48px;border:4px solid #e5e7eb;border-top-color:#38a880;border-radius:50%;animation:tSpin .8s linear infinite}
@keyframes tSpin{to{transform:rotate(360deg)}}
@media (max-width:767px){
 .termos-sec{padding:1.5rem .9rem 3rem}
 .termos-h1{font-size:1.5rem}
 .termos-head{flex-direction:column;text-align:center;padding:1.5rem 1.25rem;gap:1rem}
 .termos-org{font-size:1.25rem}
 .termos-info{grid-template-columns:1fr 1fr;padding:1.25rem}
 .termos-body{padding:1.25rem}
 .termos-acoes{flex-direction:column}
 .termos-btn{width:100%}
}
</style>
<script src="/seduc/concurso.js?v=5"></script>
<script>
(function(){
 var D={
  assistente:{edital:'Concurso Público nº 001/2026',edital2:'Edital de Abertura nº 001/2026 – PMPE',orgao:'PMPE - Polícia Militar de Pernambuco',desc:'Secretaria de Administração e Secretaria de Defesa Social de Pernambuco',vagas:'70 Oficial · 1.250 Soldado',logo:'/idcap/img/pmpe-logo.jpg',page:'/pmpe.html'},
  analista:{edital:'Concurso Público nº 002/2026',edital2:'Edital de Abertura nº 002/2026 – CBMPE',orgao:'CBMPE - Corpo de Bombeiros Militar de Pernambuco',desc:'Secretaria de Administração e Secretaria de Defesa Social de Pernambuco',vagas:'60 Oficial · 510 Soldado',logo:'/idcap/img/cbmpe-logo.jpg',page:'/cbmpe.html'}
 };
 var k=(window.SEAD_CONCURSO&&D[SEAD_CONCURSO.key])?SEAD_CONCURSO.key:'assistente', d=D[k];
 document.getElementById('t-edital').textContent=d.edital;
 document.getElementById('t-edital2').textContent=d.edital2;
 document.getElementById('t-orgao').textContent=d.orgao;
 document.getElementById('t-desc').textContent=d.desc;
 document.getElementById('t-vagas').textContent=d.vagas;
 var lg=document.getElementById('t-logo'); lg.src=d.logo; lg.alt=d.orgao;
 document.title='Termos de Inscrição - '+d.orgao+' | Instituto AOCP';
 var loader=document.getElementById('home-loader'), cb=document.getElementById('termos'), bt=document.getElementById('bt-continuar'), bv=document.getElementById('btn-voltar-termos');
 bv.setAttribute('href',d.page);
 function sync(){var on=cb.checked;bt.style.opacity=on?'1':'.45';bt.style.pointerEvents=on?'auto':'none';bt.setAttribute('aria-disabled',on?'false':'true');}
 cb.addEventListener('change',sync);sync();
 function go(u){loader.classList.add('on');setTimeout(function(){location.href=u;},700);}
 bt.addEventListener('click',function(e){e.preventDefault();if(cb.checked)go('/inscricao.html');});
 bv.addEventListener('click',function(e){e.preventDefault();go(d.page);});
 window.addEventListener('pageshow',function(ev){if(ev.persisted)loader.classList.remove('on');});
})();
</script>
'''


def build_termos():
    h = clean(open(SRC + 'inicio_src.html', encoding='utf-8').read())
    h = re.sub(r'<div class=pt-20>.*?(?=<footer>)', lambda m: TERMOS_MAIN, h, count=1, flags=re.S)
    h = h.replace('<title>Instituto AOCP - Concursos Públicos</title>', '<title>Termos de Inscrição | Instituto AOCP</title>', 1)
    finish(h, 'termos.html')


build_inicio()
build_concurso('pmpe', 'assistente', '6b0db10c', '42132750', 'PMPE - Polícia Militar de Pernambuco')
build_concurso('cbmpe', 'analista', '0785604f', 'ac588e9b', 'CBMPE - Corpo de Bombeiros Militar de Pernambuco')
build_termos()
