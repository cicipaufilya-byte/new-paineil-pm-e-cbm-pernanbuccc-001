import asyncio
import random
import time
import uuid

import httpx

API = 'http://localhost:8001/api'
random.seed(2026)

MASC = ['João', 'José', 'Carlos', 'Francisco', 'Antônio', 'Paulo', 'Lucas', 'Marcos', 'Rafael', 'Pedro', 'Gabriel',
        'Thiago', 'Diego', 'Bruno', 'Leandro', 'Rodrigo', 'Felipe', 'Matheus', 'André', 'Raimundo', 'Daniel', 'Wellington']
FEM = ['Maria', 'Ana', 'Francisca', 'Juliana', 'Patrícia', 'Aline', 'Camila', 'Fernanda', 'Larissa', 'Raimunda',
       'Jéssica', 'Letícia', 'Bruna', 'Vanessa', 'Tatiane', 'Gabriela', 'Priscila', 'Débora', 'Elaine', 'Karina', 'Luana']
MEIO = ['da Silva', 'dos Santos', 'de Souza', 'de Oliveira', 'Pereira', 'Ferreira', 'Rodrigues', 'Almeida', 'Nascimento',
        'Costa', 'Lima', 'Barbosa', 'Gomes', 'Ribeiro', 'Cardoso', 'Monteiro', 'Pantoja', 'Picanço', 'Tavares', 'Brito']
FIM = ['Silva', 'Santos', 'Souza', 'Oliveira', 'Pantoja', 'Picanço', 'Barbosa', 'Nunes', 'Moraes', 'Farias', 'Cunha',
       'Lobato', 'Corrêa', 'Rocha', 'Vasconcelos', 'Amanajás', 'Brazão', 'Duarte', 'Tavares', 'Mendes']

MACAPA = {
    'cidade': 'MACAPÁ', 'cep': (68900, 68911),
    'bairros': ['Centro', 'Buritizal', 'Trem', 'Santa Rita', 'Jesus de Nazaré', 'Laguinho', 'Pacoval', 'Beirol',
                'Congós', 'Novo Horizonte', 'Infraero', 'Zerão', 'Jardim Felicidade', 'Universidade', 'Alvorada'],
    'ruas': ['Avenida FAB', 'Rua Leopoldo Machado', 'Avenida Mendonça Furtado', 'Rua Hamilton Silva', 'Rua Tiradentes',
             'Avenida Procópio Rola', 'Rua Jovino Dinoá', 'Avenida Padre Júlio Maria Lombaerd', 'Rua Eliezer Levy',
             'Avenida Iracema Carvão Nunes', 'Rua São José', 'Avenida Ernestino Borges', 'Rua Manoel Eudóxio Pereira'],
}
SANTANA = {
    'cidade': 'SANTANA', 'cep': (68925, 68929),
    'bairros': ['Centro', 'Paraíso', 'Fonte Nova', 'Hospitalidade', 'Provedor', 'Nova Brasília', 'Area Portuária'],
    'ruas': ['Avenida Santana', 'Rua Salvador Diniz', 'Avenida Castelo Branco', 'Rua Ubaldo Figueira',
             'Avenida 15 de Novembro', 'Rua Cláudio Lúcio Monteiro'],
}
EMAILS = ['gmail.com', 'gmail.com', 'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'icloud.com']

ANALISTA = [('101', 'Analista Administrativo'), ('102', 'Analista de Comunicação Social'),
            ('103', 'Analista de Planejamento e Orçamento'), ('104', 'Analista de Tecnologia da Informação'),
            ('105', 'Analista Jurídico'), ('106', 'Analista em Relações Internacionais')]
ASSIST = [('1', 'Assistente Administrativo')]

UA_MOBILE = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; moto g(60)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; 23106RN0DA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
]
UA_DESK = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
]
IP_PREFIX = ['177.104', '177.37', '179.191', '189.45', '200.242', '187.85', '191.243', '170.233', '138.97', '45.233']


def cpf():
    n = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        s = sum(v * w for v, w in zip(n, range(len(n) + 1, 1, -1)))
        d = (s * 10) % 11
        n.append(0 if d == 10 else d)
    s = ''.join(map(str, n))
    return f'{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}'


def strip(t):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')


def pessoa(i, analista):
    fem = random.random() < 0.55
    first = random.choice(FEM if fem else MASC)
    nome = f'{first} {random.choice(MEIO)} {random.choice(FIM)}'.upper()
    loc = SANTANA if (not analista and random.random() < 0.3) else MACAPA
    cep = random.randint(*loc['cep'])
    cep_s = f'{cep}-{random.randint(0, 999):03d}'
    p = strip(nome.lower()).split()
    email = f"{p[0]}.{p[-1]}{random.randint(1, 99)}@{random.choice(EMAILS)}"
    ano = random.randint(1972, 2004) if analista else random.randint(1980, 2006)
    return {
        'NOME': nome, 'CPF': cpf(), 'DATA_NASCIMENTO': f'{random.randint(1, 28):02d}/{random.randint(1, 12):02d}/{ano}',
        'SEXO': '1' if fem else '0', 'EMAIL': email,
        'CELULAR': f'(96) 9{random.randint(8100, 9999)}-{random.randint(1000, 9999)}',
        'CEP': cep_s, 'LOGRADOURO': random.choice(loc['ruas']), 'NUMERO': str(random.randint(12, 2400)),
        'COMPLEMENTO': random.choice(['', '', '', 'Casa', 'Apto 102', 'Bloco B', 'Fundos']),
        'BAIRRO': random.choice(loc['bairros']), 'CIDADE': loc['cidade'], 'UF': 'AP',
        'DOC_TIPO': random.choice(['RG', 'RG', 'RG', 'CNH']),
        'MUNICIPIO_PROVA': 'MACAPA/AP' if (analista or loc is MACAPA) else 'SANTANA/AP', 'UF_PROVA': 'AP',
        'PORTADOR_DEFICIENCIA': '1' if random.random() < 0.06 else '0', 'atendimento_especial': '0',
    }


async def one(c, i, analista, mobile):
    d = pessoa(i, analista)
    codigo, titulo = random.choice(ANALISTA if analista else ASSIST)
    valor = 120.0 if analista else 90.0
    d['VAGA'] = codigo
    ua = random.choice(UA_MOBILE if mobile else UA_DESK)
    ip = f'{random.choice(IP_PREFIX)}.{random.randint(1, 254)}.{random.randint(1, 254)}'
    h = {'X-Forwarded-For': ip, 'User-Agent': ua, 'Content-Type': 'application/json'}
    vid = 'v_' + uuid.uuid4().hex[:16]
    cpf_d = ''.join(ch for ch in d['CPF'] if ch.isdigit())
    proto = '2026' + cpf_d[-6:]
    kind = 'Analista' if analista else 'Assistente Administrativo'
    concurso = f'SEAD/AP 2026 - IDCAP ({kind})'

    await c.post(f'{API}/track/access', headers=h, json={'page': '/', 'user_agent': ua, 'extra': {'visitor_id': vid}})
    await c.post(f'{API}/track/registration', headers=h, json={'page': '/inscricao.html', 'user_agent': ua, 'extra': {
        'nome': d['NOME'], 'cpf': d['CPF'], 'email': d['EMAIL'], 'concurso': concurso, 'stage': 'cadastro',
        'form_data': {k: v for k, v in d.items() if k not in ('VAGA', 'MUNICIPIO_PROVA', 'UF_PROVA', 'PORTADOR_DEFICIENCIA', 'atendimento_especial')},
        'visitor_id': vid}})
    await c.post(f'{API}/track/registration', headers=h, json={'page': '/confirmacao.html', 'user_agent': ua, 'extra': {
        'nome': d['NOME'], 'cpf': d['CPF'], 'email': d['EMAIL'], 'concurso': concurso, 'edital': 'SEAD_AP_26',
        'cargo_codigo': codigo, 'cargo_titulo': titulo, 'taxa': ('R$ %.2f' % valor).replace('.', ','), 'valor': valor,
        'protocolo': proto, 'stage': 'inscricao_finalizada', 'finalized': True, 'finalizado': True,
        'visitor_id': vid, 'form_data': d}})
    r = await c.post(f'{API}/pix/generate', headers=h, json={'valor': valor, 'txid': proto, 'cpf': cpf_d, 'cargo_codigo': codigo})
    ok = r.status_code == 200 and bool(r.json().get('pix_code'))
    ex = {'cpf': cpf_d, 'nome': d['NOME'], 'valor': valor, 'cargo_codigo': codigo, 'cargo_titulo': titulo}
    await c.post(f'{API}/track/pix-generated', headers=h, json={'page': '/pagamento-pix.html', 'user_agent': ua, 'extra': ex})
    await c.post(f'{API}/track/pix-copied', headers=h, json={'page': '/pagamento-pix.html', 'user_agent': ua, 'extra': ex})
    print(f'{i:02d} {kind:26s} {"mobile " if mobile else "desktop"} {d["NOME"]:40s} {d["CPF"]} {titulo} R${valor:.0f} pix={"ok" if ok else r.text[:60]}', flush=True)


async def main():
    plan = [(True, i % 2 == 0) for i in range(25)] + [(False, i % 2 == 1) for i in range(25)]
    random.shuffle(plan)
    async with httpx.AsyncClient(timeout=60) as c:
        for i, (an, mob) in enumerate(plan, 1):
            await one(c, i, an, mob)
            time.sleep(4)

asyncio.run(main())
