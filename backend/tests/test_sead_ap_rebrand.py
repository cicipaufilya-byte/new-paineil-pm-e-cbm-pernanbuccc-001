# SEAD/AP 2026 (IDCAP) rebrand regression: admin login, KPIs valor_unit=90, registration flow, PIX 90.00
import os
import re
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
TEST_CPF = '52998224725'
OLD_RE = re.compile(r'sefaz|cebraspe|alagoas|macei[oó]|auditor fiscal|r\$\s?300', re.I)


@pytest.fixture(scope='module')
def token():
    r = requests.post(f"{BASE_URL}/api/admin/auth/login", json={'username': 'donas', 'password': 'Seinao10@@'})
    assert r.status_code == 200, r.text
    t = r.json().get('token') or r.json().get('access_token')
    assert t
    return t


@pytest.fixture(scope='module')
def h(token):
    return {'Authorization': f'Bearer {token}'}


# Auth
def test_login_invalid():
    r = requests.post(f"{BASE_URL}/api/admin/auth/login", json={'username': 'donas', 'password': 'wrong'})
    assert r.status_code in (400, 401, 403)


def test_kpis_requires_auth():
    r = requests.get(f"{BASE_URL}/api/admin/dashboard/kpis")
    assert r.status_code in (401, 403)


# KPIs
def test_kpis_valor_unit_90(h):
    r = requests.get(f"{BASE_URL}/api/admin/dashboard/kpis", headers=h)
    assert r.status_code == 200
    d = r.json()
    print(d)
    assert float(d.get('valor_unit')) == 90


def test_settings_default_valor(h):
    r = requests.get(f"{BASE_URL}/api/admin/settings", headers=h)
    assert r.status_code == 200
    print({k: v for k, v in r.json().items() if 'telegram' not in k})


# Registration flow via API
def test_track_registration_finalized_creates_inscricao(h):
    payload = {'page': 'confirmacao', 'extra': {
        'nome': 'TEST_SEAD API', 'cpf': TEST_CPF, 'email': 'test_sead@example.com',
        'concurso': 'Concurso Público 001/2026 SEAD/AP', 'cargo_codigo': 'TESTAPI01',
        'cargo_titulo': 'Assistente Administrativo', 'protocolo': 'TESTPROTO', 'finalized': True}}
    r = requests.post(f"{BASE_URL}/api/track/registration", json=payload)
    assert r.status_code == 200 and r.json().get('ok')
    r = requests.get(f"{BASE_URL}/api/admin/inscriptions", headers=h)
    assert r.status_code == 200
    data = r.json()
    items = data if isinstance(data, list) else (data.get('items') or data.get('inscriptions') or data.get('data') or [])
    mine = [i for i in items if i.get('cargo_codigo') == 'TESTAPI01']
    assert mine, f'not found in {str(data)[:300]}'
    assert float(mine[0]['valor']) == 90
    assert mine[0]['edital'] == 'SEAD_AP_26'


def test_resumo_valor_90():
    r = requests.get(f"{BASE_URL}/api/inscricao/resumo/{TEST_CPF}")
    assert r.status_code == 200
    d = r.json()
    assert float(d['valor']) == 90
    assert not OLD_RE.search(str(d))


# PIX
def test_pix_configure_and_generate(h):
    s = requests.get(f"{BASE_URL}/api/admin/settings", headers=h).json()
    if not s.get('pix_key'):
        r = requests.put(f"{BASE_URL}/api/admin/settings", headers=h,
                         json={'pix_key': 'teste@exemplo.com', 'pix_nome': 'SEAD AP 2026', 'pix_cidade': 'MACAPA'})
        assert r.status_code == 200
    r = requests.post(f"{BASE_URL}/api/pix/generate", json={'valor': 300, 'txid': 'TEST123', 'cpf': TEST_CPF})
    assert r.status_code == 200, r.text
    d = r.json()
    assert float(d['valor']) == 90
    assert '540590.00' in d['pix_code']
    assert d['qr_png_base64'].startswith('iVBOR')


def test_cleanup(h):
    r = requests.get(f"{BASE_URL}/api/admin/inscriptions", headers=h)
    data = r.json()
    items = data if isinstance(data, list) else (data.get('items') or data.get('inscriptions') or data.get('data') or [])
    for i in items:
        if i.get('cargo_codigo') == 'TESTAPI01':
            requests.delete(f"{BASE_URL}/api/admin/inscriptions/{i['id']}", headers=h)
