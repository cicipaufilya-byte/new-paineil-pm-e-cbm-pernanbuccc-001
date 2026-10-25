p = '/app/frontend/public/minhas-inscricoes.html'
s = open(p).read()
a = """    fetch('/api/inscricao/resumo/'+cpf).then(function(r){return r.ok?r.json():null;}).then(function(j){
      if(!j){lista.innerHTML='';msg.textContent='Nenhuma inscrição encontrada para este CPF.';msg.style.display='block';return;}
      lista.innerHTML='';card({protocolo:j.protocolo,nome:j.nome,cpf:String(j.cpf||cpf).replace(/\\D/g,'').replace(/(\\d{3})(\\d{3})(\\d{3})(\\d{2})/,'$1.$2.$3-$4'),cargo:j.cargo_titulo,taxa:j.taxa},'/pagamento-pix.html?cpf='+cpf);
    })"""
assert a in s
s = s.replace(a, """    fetch('/api/inscricao/lista/'+cpf).then(function(r){return r.ok?r.json():null;}).then(function(j){
      if(!j||!j.items||!j.items.length){lista.innerHTML='';msg.textContent='Nenhuma inscrição encontrada para este CPF.';msg.style.display='block';return;}
      var fc=cpf.replace(/(\\d{3})(\\d{3})(\\d{3})(\\d{2})/,'$1.$2.$3-$4');
      lista.innerHTML='';
      j.items.forEach(function(it){ card({protocolo:it.protocolo,nome:it.nome,cpf:fc,cargo:it.cargo_titulo,taxa:it.taxa},'/pagamento-pix.html?cpf='+cpf+'&cargo='+encodeURIComponent(it.cargo_codigo)); });
    })""")
open(p, 'w').write(s)
print('ok')
