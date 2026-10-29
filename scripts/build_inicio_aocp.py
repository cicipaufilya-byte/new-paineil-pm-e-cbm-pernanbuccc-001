import re

src = open('/tmp/aocp.html', encoding='utf-8').read()
h = src

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
# mobile drawer (empty) removed
h = re.sub(r'<div class="w-full justify-between lg:hidden sf-hidden">.*?</ul></div></div></div>', '', h, flags=re.S)
# Voltar
h = re.sub(r'<div class="flex items-center justify-start"><a class="font-lg text-sm uppercase text-blue-900".*?Voltar</a></div>', '', h, flags=re.S)
h = h.replace('<div class="mx-auto hidden w-full justify-between lg:flex">', '<div class="mx-auto hidden w-full justify-between lg:flex top-bar">')
h = re.sub(r'<div class="mx-5 mb-10 flex items-center rounded-xl border-2 border-blue-900 p-2"><input[^>]*></div>', '<div class=mb-4></div>', h)
h = h.replace('>Concursos com Inscrições Abertas</h1>', '>Concursos com Inscrições Abertas em Pernambuco</h1>')
h = h.replace('<input class="flex-grow bg-transparent pl-5 text-xl outline-none md:pl-10"', '<input id=busca-concurso data-testid=busca-concurso-input class="flex-grow bg-transparent pl-5 text-xl outline-none md:pl-10"')

cards = '''<div class="flex min-w-full flex-col divide-gray-200 overflow-hidden px-5 pb-12 align-middle" id=lista-concursos><div class="my-2 rounded-xl bg-gray-100 p-5 font-medium text-gray-800 concurso-card" data-testid=concurso-pmpe><a href=/assistente-administrativo.html><h1 class="text-xl text-gray-800 hover:underline">PMPE - POLÍCIA MILITAR DE PERNAMBUCO</h1><p class="pt-2 font-sans text-sm font-normal hover:underline">Concurso Público nº 001/2026 - Polícia Militar de Pernambuco (PMPE) - Divulgado o Edital de Deferimento e Indeferimento das Solicitações de Isenção da Taxa de Inscrição.</p></a></div><div class="my-2 rounded-xl bg-gray-100 p-5 font-medium text-gray-800 concurso-card" data-testid=concurso-cbmpe><a href=/analista.html><h1 class="text-xl text-gray-800 hover:underline">CBMPE - CORPO DE BOMBEIROS MILITAR DE PERNAMBUCO</h1><p class="pt-2 font-sans text-sm font-normal hover:underline">Concurso Público nº 002/2026 - Corpo de Bombeiros Militar de Pernambuco (CBMPE) - Divulgado o Edital de Deferimento e Indeferimento das Solicitações de Isenção da Taxa de Inscrição.</p></a></div><p id=sem-resultado class="hidden py-6 text-center text-gray-500">Nenhum concurso encontrado.</p></div>'''
h = re.sub(r'<div class="flex min-w-full flex-col divide-gray-200 overflow-hidden px-5 pb-12 align-middle">.*?</a></div></div>', cards, h, count=1, flags=re.S)

# external links -> internal
h = re.sub(r'href=https://www\.institutoaocp\.org\.br/(?=[ >])', 'href=/inicio.html', h)
h = re.sub(r'href=https://www\.institutoaocp\.org\.br/concursos/status/inscricoes-abertas', 'href=/inicio.html', h)
h = re.sub(r'href="?https?://[^ >"]+"?', 'href=#', h)
h = h.replace(' target=_blank', '')

extra = '''<style>
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
@media (max-width:639px){footer.footer{grid-template-columns:1fr!important;grid-auto-flow:row!important}}
</style>
<script>
(function(){
 try{var v=localStorage.getItem('visitor_id');if(!v){v='v_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);localStorage.setItem('visitor_id',v);}
 fetch('/api/track/access',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({page:location.pathname,user_agent:navigator.userAgent,extra:{visitor_id:v}})}).catch(function(){});}catch(e){}
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href="#"]');if(a)e.preventDefault();});
})();
</script>
'''
h = h.rstrip() + '\n' + extra
h = h.replace('<title>Instituto AOCP - Concursos Públicos</title>', '<title>Instituto AOCP - Concursos Públicos</title><meta name=viewport content="width=device-width, initial-scale=1">', 1)
open('/app/frontend/public/inicio.html', 'w', encoding='utf-8').write(h)
print(len(src), len(h))
print('external left:', re.findall(r'https?://(?!www\.w3\.org)[^ >"\')]+', re.sub(r'data:[^"\')]+', '', h))[:20])
