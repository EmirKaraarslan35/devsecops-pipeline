"""
DevSecOps Pipeline Demo - Testler
==================================
Basit birim testleri. Pipeline'da test aşamasında çalıştırılır.
"""

import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """Flask test client'ı oluşturur."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Ana sayfa endpoint'inin çalıştığını test eder."""
    response = client.get("/")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["durum"] == "calisiyor"
    assert "versiyon" in data


def test_health_endpoint(client):
    """Sağlık kontrolü endpoint'inin çalıştığını test eder."""
    response = client.get("/health")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["durum"] == "saglikli"


def test_hash_endpoint(client):
    """Hash endpoint'inin SHA-256 ile çalıştığını test eder."""
    response = client.post(
        "/hash",
        data=json.dumps({"text": "test123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["hash_algoritmasi"] == "SHA-256"
    assert len(data["hash"]) == 64  # SHA-256 = 64 hex karakter


def test_hash_endpoint_missing_text(client):
    """Hash endpoint'ine text olmadan istek gönderildiğini test eder."""
    response = client.post(
        "/hash",
        data=json.dumps({}),
        content_type="application/json"
    )

    assert response.status_code == 400


def test_config_endpoint(client):
    """Config endpoint'inin ortam değişkenlerinden okuduğunu test eder."""
    response = client.get("/config")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "db_host" in data
    assert "db_port" in data
