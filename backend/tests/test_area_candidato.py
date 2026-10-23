# Área do Candidato: consulta por CPF via /api/inscricao/resumo/{cpf}
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
CPF = '52998224725'


@pytest.fixture(scope='module')
def admin():
    s = requests.Session()
    r = s.post(f"{BASE_URL}/api/admin/auth/login", json={'username': 'donas', 'password': 'Seinao10@@'})
    if r.status_code != 200:
        pytest.skip('admin login failed')
    tok = r.json().get('token') or r.json().get('access_token')
    s.headers['Authorization'] = f'Bearer {tok}'
    yield s
    # cleanup
    items = s.get(f"{BASE_URL}/api/admin/inscriptions", params={'q': CPF, 'limit': 200}).json().get('items', [])
    for it in items:
        if it.get('cpf') == CPF:
            s.delete(f"{BASE_URL}/api/admin/inscriptions/{it['id']}")
    s.delete(f"{BASE_URL}/api/admin/cadastros/{CPF}")


def test_resumo_not_found():
    r = requests.get(f"{BASE_URL}/api/inscricao/resumo/11144477735")
    assert r.status_code == 404


def test_resumo_after_registration(admin):
    r = requests.post(f"{BASE_URL}/api/track/registration", json={'page': '/inscricao.html', 'extra': {
        'finalized': True, 'stage': 'inscricao_finalizada', 'cpf': '529.982.247-25',
        'nome': 'TEST_AREA CANDIDATO', 'cargo_titulo': 'Analista Jurídico'}})
    assert r.status_code == 200
    r = requests.get(f"{BASE_URL}/api/inscricao/resumo/529.982.247-25")
    assert r.status_code == 200
    d = r.json()
    assert d['nome'] == 'TEST_AREA CANDIDATO'
    assert d['cpf'] == CPF
    assert d['cargo_titulo'] == 'Analista Jurídico'
    assert d['taxa'] == 'R$ 120,00'
    assert d['valor'] == 120.0
