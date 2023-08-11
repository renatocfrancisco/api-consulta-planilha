import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_data_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Hello world"}


def test_post_data_missing_keys(client):
    data = {"uf": ["SP"], "idadeMin": 18, "idadeMax": 30}
    response = client.post("/", json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Data has missing keys"}


def test_post_data_invalid_values(client):
    data = {
        "uf": ["TO", "ES", "RO"],
        "idadeMin": "70",
        "esp": [21, 41],
        "banco_emp": [1, 2],
        "banco_pgto": [104, 237],
    }
    response = client.post("/", json=data)
    assert response.status_code == 400
    assert response.json.get("message") == "Data has invalid values"


def test_post_data_not_received(client):
    data = {}
    response = client.post("/", json=data)
    assert response.status_code == 400
    assert response.json.get("message") == "No data received"


def test_post_return_csv_or_not_found(client):
    data = {
        "uf": ["RR"],
        "idadeMin": 80,
        "idadeMax": 80,
        "parcelaMin": 50,
        "parcelaMax": 400,
        "parcelasPagasMin": 70,
        "parcelasPagasMax": 500,
        "jurosMin": 1,
        "jurosMax": 2,
        "esp": [21, 41],
        "banco_emp": [1, 2],
        "banco_pgto": [104, 237],
    }
    response = client.post("/", json=data)
    assert response.status_code == 200 or 404

    assert b"No data found" in response.data or (
        response.headers.get("Content-Disposition") == "attachment; filename=data.csv"
        and response.headers.get("Content-Type") == "text/csv; charset=utf-8"
        and response.headers.get("Content-Length") is not "0"
    )
