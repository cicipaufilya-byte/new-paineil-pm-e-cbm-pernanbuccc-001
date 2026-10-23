# READ-ONLY regression: validates the 50 seeded inscriptions (iteration_68). Never writes data.
import os
import re
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
LOG = '/app/memory/seed_50.log'


def _seed():
    rows = []
    for line in open(LOG, encoding='utf-8'):
        m = re.search(r'(\d{3}\.\d{3}\.\d{3}-\d{2}).*R\$(\d+)', line)
        dev = 'mobile' if ' mobile ' in line else 'desktop'
        rows.append({'cpf': re.sub(r'\D', '', m.group(1)), 'valor': float(m.group(2)), 'device': dev})
    return rows


SEED = _seed()


@pytest.fixture(scope='module')
def client():
    s = requests.Session()
    r = s.post(f'{BASE_URL}/api/admin/auth/login', json={'username': 'donas', 'password': 'Seinao10@@'})
    if r.status_code != 200:
        pytest.skip(f'login failed {r.status_code} {r.text[:200]}')
    tok = r.json().get('token') or r.json().get('access_token')
    s.headers.update({'Authorization': f'Bearer {tok}'})
    return s


def test_seed_log_shape():
    assert len(SEED) == 50
    assert sum(1 for r in SEED if r['valor'] == 120) == 25
    assert sum(1 for r in SEED if r['valor'] == 90) == 25
    assert sum(1 for r in SEED if r['device'] == 'mobile') == 25


# Dashboard KPIs
def test_kpis(client):
    d = client.get(f'{BASE_URL}/api/admin/dashboard/kpis').json()
    print(d)
    assert d['inscricoes'] == 50
    assert d['pix_gerados'] == 50
    assert d['pix_copiados'] == 50
    assert d['pix_baixados'] == 0
    assert d['valor_total'] == 5250.0
    assert d['valor_copiados'] == 5250.0
    assert d['acessos'] == 50


# Inscription list
def test_inscriptions_list(client):
    d = client.get(f'{BASE_URL}/api/admin/inscriptions').json()
    items = d['items']
    assert d['total'] == 50 and len(items) == 50
    by = {i['cpf']: i for i in items}
    for r in SEED:
        it = by.get(r['cpf'])
        assert it, f"missing {r['cpf']}"
        assert it['valor'] == r['valor'], (r, it['valor'])
        assert it['status'] == 'PIX copiado', it['status']
        assert it['device'] == r['device'], (r['cpf'], it['device'])
        assert it.get('nome') and it.get('cargo_titulo')
        assert '_id' not in it and 'senha_hash' not in it
        assert not it.get('paid') and 'pago' not in str(it.get('status', '')).lower()
    assert sum(i['valor'] for i in items) == 5250.0


# Accesses: cities Macapá/Santana, devices
def test_accesses(client):
    d = client.get(f'{BASE_URL}/api/admin/accesses').json()
    items = d['items']
    assert d['total'] == 50
    cities = {(i.get('city') or '') for i in items}
    print('cities', cities)
    assert cities <= {'Macapá', 'Santana'}
    assert all((i.get('uf') or '') == 'AP' for i in items)
    mob = sum(1 for i in items if i['device'] == 'mobile')
    print('mobile accesses', mob)
    assert 20 <= mob <= 30


def test_funnel_devices_and_locations(client):
    r = client.get(f'{BASE_URL}/api/admin/dashboard/funnel-devices')
    assert r.status_code == 200
    print('funnel-devices', r.json())
    r2 = client.get(f'{BASE_URL}/api/admin/dashboard/locations')
    assert r2.status_code == 200
    print('locations', r2.json())


# Public resumo used by Área do Candidato
@pytest.mark.parametrize('cpf,valor,cargo', [
    ('48876634479', 120.0, 'Tecnologia da Informa'),
    ('97684697811', 90.0, 'Assistente Administrativo'),
])
def test_resumo(cpf, valor, cargo):
    r = requests.get(f'{BASE_URL}/api/inscricao/resumo/{cpf}')
    assert r.status_code == 200
    d = r.json()
    print(d)
    assert d['valor'] == valor
    assert cargo in d['cargo_titulo']


@pytest.mark.parametrize('cpf', ['48876634479', '97684697811'])
def test_check_candidate(cpf):
    r = requests.post(f'{BASE_URL}/api/auth/check-candidate', json={'cpf': cpf})
    assert r.status_code == 200, r.text
    assert r.json()['cadastro']['cpf'] == cpf
