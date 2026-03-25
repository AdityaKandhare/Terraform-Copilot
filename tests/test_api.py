from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate():
    response = client.get("/generate?prompt=Create S3 bucket")
    assert response.status_code == 200