import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import engine, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_countries_requires_key(client):
    r = client.get("/api/v1/countries")
    assert r.status_code == 401

def test_admin_create_key(client):
    r = client.post("/api/admin/keys", params={"name": "test"}, headers={"X-API-Key": "dummy"})
    assert r.status_code in [200, 201, 401]
