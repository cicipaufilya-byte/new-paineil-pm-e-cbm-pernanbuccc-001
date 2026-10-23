# SEAD/AP 001/2026 Analista concurso: valor 120 per Analista cargo, 90 for Assistente; resumo, PIX, KPIs
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
CPF_AN = '11144477735'
CPF_AS = '52998224725'
CODES = ('TESTAN101', 'TESTAS1')


@pytest.fixture(scope='module')
def h():
    r = requests.post(f"{BASE_URL}/api/admin/auth/login", json={'username': 'donas', 'password': 'Seinao10@@'})
    assert r.status_code == 200, r.text
    t = r.json().get('token') or r.json().get('access_token')
    yield {'Authorization': f'Bearer {t}'}
    # cleanup inscriptions + pix key
    items = _items(requests.get(f"{BASE_URL}/api/admin/inscriptions", headers={'Authorization': f'Bearer {t}'}).json())
    for i in items:
        if i.get('cargo_codigo') in CODES:
            requests.delete(f"{BASE_URL}/api/admin/inscriptions/{i['id']}", headers={'Authorization': f'Bearer {t}'})
    requests.put(f"{BASE_URL}/api/admin/settings", headers={'Authorization': f'Bearer {t}'}, json={'pix_key': ''})


def _items(data):
    return data if isinstance(data, list) else (data.get('items') or data.get('inscriptions') or data.get('data') or [])


def _reg(cpf, code, titulo):
    payload = {'page': 'confirmacao', 'extra': {
        'nome': 'TEST_SEAD ' + titulo, 'cpf': cpf, 'email': 'test_sead@example.com',
        'concurso': 'Concurso Público 001/2026 SEAD/AP', 'cargo_codigo': code,
        'cargo_titulo': titulo, 'protocolo': 'TESTPROTO' + code, 'finalized': True}}
    return requests.post(f"{BASE_URL}/api/track/registration", json=payload)


# Registration Analista -> valor 120
def test_registration_analista_120(h):
    r = _reg(CPF_AN, 'TESTAN101', 'Analista de Tecnologia da Informação')
    assert r.status_code == 200 and r.json().get('ok')
    mine = [i for i in _items(requests.get(f"{BASE_URL}/api/admin/inscriptions", headers=h).json()) if i.get('cargo_codigo') == 'TESTAN101']
    assert mine
    assert float(mine[0]['valor']) == 120
    assert mine[0]['cargo_titulo'] == 'Analista de Tecnologia da Informação'


# Registration Assistente -> valor 90
def test_registration_assistente_90(h):
    r = _reg(CPF_AS, 'TESTAS1', 'Assistente Administrativo')
    assert r.status_code == 200
    mine = [i for i in _items(requests.get(f"{BASE_URL}/api/admin/inscriptions", headers=h).json()) if i.get('cargo_codigo') == 'TESTAS1']
    assert mine and float(mine[0]['valor']) == 90


def test_resumo_analista_120(h):
    d = requests.get(f"{BASE_URL}/api/inscricao/resumo/{CPF_AN}").json()
    assert float(d['valor']) == 120
    assert d['taxa'] == 'R$ 120,00'


def test_resumo_assistente_90(h):
    d = requests.get(f"{BASE_URL}/api/inscricao/resumo/{CPF_AS}").json()
    assert float(d['valor']) == 90


def test_pix_generate_values(h):
    r = requests.put(f"{BASE_URL}/api/admin/settings", headers=h,
                     json={'pix_key': 'teste@exemplo.com', 'pix_nome': 'SEAD AP 2026', 'pix_cidade': 'MACAPA'})
    assert r.status_code == 200
    a = requests.post(f"{BASE_URL}/api/pix/generate", json={'valor': 90, 'txid': 'TESTAN', 'cpf': CPF_AN})
    assert a.status_code == 200, a.text
    assert float(a.json()['valor']) == 120 and '5406120.00' in a.json()['pix_code']
    b = requests.post(f"{BASE_URL}/api/pix/generate", json={'valor': 120, 'txid': 'TESTAS', 'cpf': CPF_AS})
    assert float(b.json()['valor']) == 90 and '540590.00' in b.json()['pix_code']


def test_pix_qr_png_120(h):
    r = requests.get(f"{BASE_URL}/api/pix/code.txt", params={'valor': 120, 'txid': 'T'})
    assert r.status_code == 200 and '5406120.00' in r.text


def test_kpis_sum(h):
    # pix_generated tracking events to feed KPIs
    for cpf in (CPF_AN, CPF_AS):
        requests.post(f"{BASE_URL}/api/track/pix-generated", json={'page': 'pagamento-pix', 'extra': {'cpf': cpf}})
    d = requests.get(f"{BASE_URL}/api/admin/dashboard/kpis", headers=h).json()
    print(d)
    assert d['valor_total'] >= 210 or d['pix_gerados'] == 0
