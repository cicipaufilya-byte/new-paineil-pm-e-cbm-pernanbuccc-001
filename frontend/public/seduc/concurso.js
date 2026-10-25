(function(){
  var C = {
    assistente: {
      nome: 'Assistente Administrativo',
      nivel: 'Nível Médio',
      cargos: [{v: '1', t: 'Assistente Administrativo', p: '90.00'}],
      cidades: [['MACAPA/AP', 'MACAPÁ/AP'], ['SANTANA/AP', 'SANTANA/AP']],
      pagina: '/assistente-administrativo.html'
    },
    analista: {
      nome: 'Analista',
      nivel: 'Nível Superior',
      cargos: [
        {v: '101', t: 'Analista Administrativo', p: '120.00'},
        {v: '102', t: 'Analista de Comunicação Social', p: '120.00'},
        {v: '103', t: 'Analista de Planejamento e Orçamento', p: '120.00'},
        {v: '104', t: 'Analista de Tecnologia da Informação', p: '120.00'},
        {v: '105', t: 'Analista Jurídico', p: '120.00'},
        {v: '106', t: 'Analista em Relações Internacionais', p: '120.00'}
      ],
      cidades: [['MACAPA/AP', 'MACAPÁ/AP']],
      pagina: '/analista.html'
    }
  };
  C.todos = {
    nome: 'Assistente Administrativo', nivel: '', pagina: '/',
    cargos: C.assistente.cargos.concat(C.analista.cargos),
    cidades: C.assistente.cidades, todos: true
  };
  var key = 'assistente';
  try {
    var q = new URLSearchParams(location.search).get('c');
    if (q && C[q]) { key = q; localStorage.setItem('concurso_sel', q); }
    else { var s = localStorage.getItem('concurso_sel'); if (s && C[s]) key = s; }
  } catch (e) {}
  var cur = C[key];
  window.SEAD_CONCURSO = {key: key, cfg: cur};

  function fill(){
    document.querySelectorAll('[data-c]').forEach(function(el){
      var k = el.getAttribute('data-c');
      if (cur[k] != null) el.textContent = cur[k];
    });
    var vaga = document.getElementById('VAGA');
    if (vaga && !vaga.dataset.cfg) {
      vaga.dataset.cfg = key;
      var opt = function(c){ return '<option value="' + c.v + '" data-price="' + c.p + '">' + c.t + '</option>'; };
      vaga.innerHTML = '<option value="">Selecione</option>'
        + '<optgroup label="Assistente Administrativo (Nível Médio) - R$ 90,00">' + C.assistente.cargos.map(opt).join('') + '</optgroup>'
        + '<optgroup label="Analista (Nível Superior) - R$ 120,00">' + C.analista.cargos.map(opt).join('') + '</optgroup>';
      var setCidades = function(){
        var an = /^10\d$/.test(vaga.value);
        cur.nome = an ? 'Analista' : 'Assistente Administrativo';
        var mp = document.getElementById('MUNICIPIO_PROVA'); if (!mp) return;
        var list = an ? C.analista.cidades : C.assistente.cidades, prev = mp.value;
        mp.innerHTML = (list.length > 1 ? '<option value="">Selecione</option>' : '') + list.map(function(c){ return '<option value="' + c[0] + '" data-uf="AP">' + c[1] + '</option>'; }).join('');
        mp.dataset.cfg = key;
        if (list.some(function(c){ return c[0] === prev; })) mp.value = prev; else if (list.length === 1) mp.value = list[0][0];
      };
      vaga.addEventListener('change', setCidades);
      setCidades();
    }
    if (vaga && !vaga.dataset.cfg) {
      vaga.dataset.cfg = key;
      vaga.innerHTML = (cur.cargos.length > 1 ? '<option value="">Selecione</option>' : '') +
        cur.cargos.map(function(c){ return '<option value="' + c.v + '" data-price="' + c.p + '">' + c.t + '</option>'; }).join('');
      if (cur.cargos.length === 1) vaga.value = cur.cargos[0].v;
    }
    var mp = document.getElementById('MUNICIPIO_PROVA');
    if (mp && !mp.dataset.cfg) {
      mp.dataset.cfg = key;
      mp.innerHTML = (cur.cidades.length > 1 ? '<option value="">Selecione</option>' : '') +
        cur.cidades.map(function(c){ return '<option value="' + c[0] + '" data-uf="AP">' + c[1] + '</option>'; }).join('');
      if (cur.cidades.length === 1) mp.value = cur.cidades[0][0];
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill); else fill();
  window.addEventListener('load', function(){
    var v=document.getElementById('VAGA'); if (!v) return;
    { var sv=''; try{ sv=(JSON.parse(localStorage.getItem('inscricao_dados')||'{}').VAGA)||''; }catch(e){} v.value = sv; v.dispatchEvent(new Event('change', {bubbles:true})); }
    if (v.selectedIndex < 0) v.selectedIndex = 0;
  });
})();
