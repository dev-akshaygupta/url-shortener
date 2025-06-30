from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten_and_redirect():
    response = client.post("/shorten", json={"long_url": "https://openai.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data

    # Now test GET redirect
    short_code = data["short_code"]
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code in (302, 307, 200)
