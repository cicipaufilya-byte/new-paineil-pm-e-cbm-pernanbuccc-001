# Inscriptions date filter (date_from/date_to) - read-only tests
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')


@pytest.fixture(scope='module')
def client():
    s = requests.Session()
    r = s.post(f"{BASE_URL}/api/admin/auth/login", json={'username': 'donas', 'password': 'Seinao10@@'})
    if r.status_code != 200:
        pytest.skip(f"login failed {r.status_code}")
    tok = r.json().get('token') or r.json().get('access_token')
    if tok:
        s.headers['Authorization'] = f'Bearer {tok}'
    return s


def _get(c, **p):
    return c.get(f"{BASE_URL}/api/admin/inscriptions", params=p)


def test_no_filter(client):
    r = _get(client)
    assert r.status_code == 200
    assert r.json()['total'] == 50


def test_today(client):
    d = _get(client, date_from='2026-10-23', date_to='2026-10-23').json()
    assert d['total'] == 50 and len(d['items']) == 50


def test_yesterday_zero(client):
    d = _get(client, date_from='2026-10-22', date_to='2026-10-22').json()
    assert d['total'] == 0 and d['items'] == []


def test_range_past(client):
    assert _get(client, date_from='2026-10-20', date_to='2026-10-22').json()['total'] == 0


def test_only_from(client):
    assert _get(client, date_from='2026-10-17').json()['total'] == 50
    assert _get(client, date_from='2026-10-24').json()['total'] == 0


def test_only_to(client):
    assert _get(client, date_to='2026-10-23').json()['total'] == 50
    assert _get(client, date_to='2026-10-22').json()['total'] == 0


def test_bad_dates(client):
    assert _get(client, date_from='bad').status_code == 400
    assert _get(client, date_to='2026-13-01').status_code == 400


def test_combine_q(client):
    d = _get(client, date_from='2026-10-23', date_to='2026-10-23', q='JULIANA').json()
    allq = _get(client, q='JULIANA').json()
    assert d['total'] == allq['total']
    assert all('JULIANA' in i['nome'].upper() for i in d['items'])


def test_unauth():
    r = requests.get(f"{BASE_URL}/api/admin/inscriptions", params={'date_from': '2026-10-23'})
    assert r.status_code in (401, 403)
