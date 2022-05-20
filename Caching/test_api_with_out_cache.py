from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_trend_hashtags():
    response = client.get("/api/v1/todo/find/all")
    assert response.status_code == 200
