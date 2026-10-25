p = '/app/frontend/public/minhas-inscricoes.html'
s = open(p).read()
s = s.replace("    lista.innerHTML='';lista.appendChild(el);\n  }", "    lista.appendChild(el);\n  }")
s = s.replace("      card({protocolo:j.protocolo,nome:j.nome,", "      lista.innerHTML='';card({protocolo:j.protocolo,nome:j.nome,")
a = """    card({protocolo:d.__protocolo,nome:d.NOME,cpf:d.CPF,cargo:d.__vaga_label||d.VAGA,taxa:d.__taxa},'/inscricao-realizada.html');"""
assert a in s
s = s.replace(a, """    var localCargo=String(d.__cargo_codigo||d.VAGA||'');
    card({protocolo:d.__protocolo,nome:d.NOME,cpf:d.CPF,cargo:d.__vaga_label||d.VAGA,taxa:d.__taxa},'/inscricao-realizada.html');
    var cpfD=String(d.CPF).replace(/\\D/g,'');
    fetch('/api/inscricao/lista/'+cpfD).then(function(r){return r.ok?r.json():null;}).then(function(j){
      if(!j||!j.items||!j.items.length)return;
      lista.innerHTML='';
      j.items.forEach(function(it){
        var mine=String(it.cargo_codigo)===localCargo;
        card({protocolo:it.protocolo,nome:it.nome,cpf:d.CPF,cargo:it.cargo_titulo,taxa:it.taxa}, mine?'/inscricao-realizada.html':'/pagamento-pix.html?cpf='+cpfD+'&cargo='+encodeURIComponent(it.cargo_codigo));
      });
    }).catch(function(){});
    var nb=document.getElementById('btn-nova-inscricao');nb.style.display='inline-flex';
    nb.addEventListener('click',function(e){
      e.preventDefault();
      try{
        var x=JSON.parse(localStorage.getItem('inscricao_dados')||'{}');
        Object.keys(x).forEach(function(k){ if(k.charAt(0)==='_'&&k.charAt(1)==='_') delete x[k]; });
        ['VAGA','MUNICIPIO_PROVA','UF_PROVA','PORTADOR_DEFICIENCIA','atendimento_especial','termo','aceito_termos'].forEach(function(k){ delete x[k]; });
        localStorage.setItem('inscricao_dados',JSON.stringify(x));
        localStorage.setItem('concurso_sel','todos');
      }catch(_){}
      location.href='/dados-inscricao.html?c=todos';
    });""")
a = """ <a class="back" href="/" data-testid="btn-voltar">&larr; Voltar</a>"""
assert a in s
s = s.replace(a, """ <div class="acoes-mi"><a class="back" href="/" data-testid="btn-voltar">&larr; Voltar</a><a class="back nova" href="/dados-inscricao.html?c=todos" id="btn-nova-inscricao" data-testid="btn-nova-inscricao" style="display:none">+ Nova Inscrição</a></div>""")
s = s.replace(".back{display", ".acoes-mi{display:flex;gap:12px;flex-wrap:wrap;align-items:center}\n.acoes-mi .back{margin-top:0!important}\n.back.nova{background:#3576fb!important;color:#fff!important;border-color:#3576fb!important}\n.back{display", 1)
open(p, 'w').write(s)

p = '/app/frontend/public/pagamento-pix.html'
s = open(p).read()
a = "has = !!(e && e.CPF) && String(e.CPF).replace(/\\D/g,'') === cpf;"
assert a in s
s = s.replace(a, "has = !!(e && e.CPF) && String(e.CPF).replace(/\\D/g,'') === cpf && (!params.get('cargo') || String(e.__cargo_codigo||e.VAGA||'') === params.get('cargo'));")
a = "fetch(window.location.origin + '/api/inscricao/resumo/' + cpf)"
assert a in s
s = s.replace(a, "fetch(window.location.origin + '/api/inscricao/resumo/' + cpf + (params.get('cargo') ? '?cargo=' + encodeURIComponent(params.get('cargo')) : ''))")
open(p, 'w').write(s)
print('ok')
