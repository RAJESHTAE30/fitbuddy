from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FITBUDDY" in response.text

def test_admin_page():
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Dashboard login" in response.text
