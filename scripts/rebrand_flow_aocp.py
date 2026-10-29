import re

P = '/app/frontend/public/'
FILES = ['inscricao.html', 'dados-inscricao.html', 'pagamento-pix.html', 'inscricao-realizada.html', 'minhas-inscricoes.html', 'confirmacao.html']
CJS = '<script src="/seduc/concurso.js?v=6"></script>'

R = [
    (' - SEAD/AP 2026 | IDCAP</title>', ' | Instituto AOCP</title>'),
    ('Concurso Público SEAD/AP 001/2026 - Secretaria de Estado da Administração do Amapá | IDCAP', 'Concursos PMPE e CBMPE 2026 | Instituto AOCP'),
    ('SEAD/AP, concurso público, Assistente Administrativo, IDCAP, 2026', 'PMPE, CBMPE, concurso público, Pernambuco, Instituto AOCP, 2026'),
    ('content="IDCAP" name="author"', 'content="Instituto AOCP" name="author"'),
    ('<h3 class="vn-keep">SEAD/AP 2026</h3>', '<h3 class="vn-keep" data-c="titulo">PMPE 2026</h3>'),
    ('<p class="vn-sub">Secretaria de Estado da Administração do Amapá</p>', '<p class="vn-sub" data-c="orgao">Polícia Militar de Pernambuco</p>'),
    ('<h3>SEAD/AP 2026</h3>', '<h3>Concursos Pernambuco 2026</h3>'),
    ('Inscrições de <b>08/10/2026</b> a <b>29/10/2026</b>', 'Inscrições até <b>05/11/2026</b>, às 23h59'),
    ('O IDCAP atende', 'O Instituto AOCP atende'),
    ('© IDCAP — SEAD/AP 2026', '© Instituto AOCP — Pernambuco 2026'),
    ("var CONCURSO = 'SEAD/AP 2026 - IDCAP (' + ((window.SEAD_CONCURSO && SEAD_CONCURSO.cfg.nome) || 'Assistente Administrativo') + ')';",
     "var CONCURSO = ((window.SEAD_CONCURSO && SEAD_CONCURSO.cfg.titulo) || 'PMPE 2026') + ' - Instituto AOCP';"),
    ("var CONCURSO = 'SEAD/AP 2026 - IDCAP';", "var CONCURSO = ((window.SEAD_CONCURSO && SEAD_CONCURSO.cfg.titulo) || 'PMPE 2026') + ' - Instituto AOCP';"),
    ("'SEAD_AP_26'", "((window.SEAD_CONCURSO && SEAD_CONCURSO.key === 'cbmpe') ? 'CBMPE_26' : 'PMPE_26')"),
    ('<option value="1" selected="">SEAD/AP 2026 - Edital nº 001/2026</option>', '<option value="1" selected="" data-c="edital_opt">PMPE 2026 - Concurso Público nº 001/2026</option>'),
    ('<option value="1" data-price="90.00" selected="">Assistente Administrativo</option>', '<option value="">Selecione</option>'),
    ('id="UF_PROVA" name="UF_PROVA" value="AP"', 'id="UF_PROVA" name="UF_PROVA" value="PE"'),
    ('Edital nº 001/2026 – SEAD/AP', '<span data-c="edital_curto">Edital nº 001/2026 – PMPE</span>'),
    ('Sites IDCAP', 'Sites AOCP'),
    ('<span>IDCAP</span>', '<span>AOCP</span>'),
    ('atendimento@idcap.org.br', 'candidato@institutoaocp.org.br'),
    ('alt="IDCAP"', 'alt="Instituto AOCP"'),
    ('IDCAP — Instituto de Desenvolvimento e Capacitação', 'Instituto AOCP'),
    ('margin-top:4px;">SEAD/AP 2026</div>', 'margin-top:4px;" data-c="titulo">PMPE 2026</div>'),
    ('Secretaria de Estado da Administração do Amapá - Edital nº 001/2026', '<span data-c="orgao_edital">Polícia Militar de Pernambuco - Edital nº 001/2026</span>'),
    ('src="/cebraspe-logo.webp"', 'src="/idcap/img/aocp-logo.png"'),
    ('Secretaria de Estado da Administração do Amapá', 'Governo do Estado de Pernambuco'),
    ('SEAD/AP 2026', 'PMPE / CBMPE 2026'),
    ('29/10/2026', '05/11/2026'),
]

for f in FILES:
    h = open(P + f, encoding='utf-8').read()
    for a, b in R:
        h = h.replace(a, b)
    h = re.sub(r'<option value="(MACAPA|SANTANA)/AP" data-uf="AP">[^<]*</option>\s*', '', h)
    h = h.replace('<script src="/seduc/concurso.js?v=4"></script>', CJS)
    if CJS not in h and f != 'minhas-inscricoes.html':
        h = h.replace('<script src="/seduc/seduc-theme.js', CJS + '\n<script src="/seduc/seduc-theme.js', 1)
    h = h.replace('/seduc/seduc-theme.js?v=46', '/seduc/seduc-theme.js?v=47')
    open(P + f, 'w', encoding='utf-8').write(h)
    left = re.findall(r'(?i).{0,40}(idcap|sead|amap[aá]|macap|assistente|analista).{0,30}', re.sub(r'<style.*?</style>|data:[^"\')]+', '', h, flags=re.S))
    print(f, 'restante:', len(left), left[:6])
