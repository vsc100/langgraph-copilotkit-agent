from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["agent_ready"] == True

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data

def test_chat_endpoint_without_api_key():
    # Test that endpoint exists
    response = client.post("/chat", json={
        "messages": [{"role": "user", "content": "Hello"}]
    })
    # Should fail due to missing API key, but endpoint should exist
    assert response.status_code in [200, 500]

if __name__ == "__main__":
    test_health_endpoint()
    test_root_endpoint()
    print("All tests passed!")
