(function(){
  var CIDADES = [['RECIFE/PE', 'RECIFE / REGIÃO METROPOLITANA/PE'], ['ARCOVERDE/PE', 'ARCOVERDE/PE'], ['CARUARU/PE', 'CARUARU/PE'], ['PETROLINA/PE', 'PETROLINA/PE']];
  var C = {
    pmpe: {
      titulo: 'PMPE 2026', sigla: 'PMPE', orgao: 'Polícia Militar de Pernambuco',
      edital_opt: 'PMPE 2026 - Concurso Público nº 001/2026',
      edital_curto: 'Edital nº 001/2026 – PMPE',
      orgao_edital: 'Polícia Militar de Pernambuco - Edital nº 001/2026',
      cargos: [
        {v: '201', t: 'Soldado (Praça da Polícia Militar QPMG)', p: '180.00'},
        {v: '401', t: '2º Tenente (Oficial da Polícia Militar QOPM)', p: '220.00'},
        {v: '402', t: '2º Tenente (Oficial da Polícia Militar QOM) Clínica Geral', p: '220.00'},
        {v: '403', t: '2º Tenente (Oficial da Polícia Militar QOM) Cirurgia Geral', p: '220.00'},
        {v: '404', t: '2º Tenente (Oficial da Polícia Militar QOD) Dentista', p: '220.00'}
      ],
      pagina: '/pmpe.html'
    },
    cbmpe: {
      titulo: 'CBMPE 2026', sigla: 'CBMPE', orgao: 'Corpo de Bombeiros Militar de Pernambuco',
      edital_opt: 'CBMPE 2026 - Concurso Público nº 002/2026',
      edital_curto: 'Edital nº 002/2026 – CBMPE',
      orgao_edital: 'Corpo de Bombeiros Militar de Pernambuco - Edital nº 002/2026',
      cargos: [
        {v: '201', t: 'Soldado do Corpo de Bombeiros Militar', p: '180.00'},
        {v: '401', t: '2º Tenente do Corpo de Bombeiros Militar', p: '220.00'}
      ],
      pagina: '/cbmpe.html'
    }
  };
  var ALIAS = {assistente: 'pmpe', analista: 'cbmpe'};
  function norm(k){ k = ALIAS[k] || k; return C[k] ? k : ''; }
  var key = 'pmpe';
  try {
    var q = norm(new URLSearchParams(location.search).get('c') || '');
    if (q) { key = q; localStorage.setItem('concurso_sel', q); }
    else { var s = norm(localStorage.getItem('concurso_sel') || ''); if (s) { key = s; localStorage.setItem('concurso_sel', s); } }
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
      vaga.innerHTML = '<option value="">Selecione</option>' + cur.cargos.map(function(c){
        return '<option value="' + c.v + '" data-price="' + c.p + '">' + c.v + '  -  ' + c.t + '  -  R$ ' + c.p.replace('.', ',') + '</option>';
      }).join('');
    }
    var mp = document.getElementById('MUNICIPIO_PROVA');
    if (mp && !mp.dataset.cfg) {
      mp.dataset.cfg = key;
      var prev = mp.value;
      mp.innerHTML = '<option value="">Selecione</option>' + CIDADES.map(function(c){ return '<option value="' + c[0] + '" data-uf="PE">' + c[1] + '</option>'; }).join('');
      if (CIDADES.some(function(c){ return c[0] === prev; })) mp.value = prev;
    }
    var uf = document.getElementById('UF_PROVA'); if (uf) uf.value = 'PE';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill); else fill();
  window.addEventListener('load', function(){
    var v = document.getElementById('VAGA'); if (!v) return;
    var sv = ''; try { sv = (JSON.parse(localStorage.getItem('inscricao_dados') || '{}').VAGA) || ''; } catch (e) {}
    v.value = sv; v.dispatchEvent(new Event('change', {bubbles: true}));
    if (v.selectedIndex < 0) v.selectedIndex = 0;
  });
})();
