"""
Ping Tests
"""

from fastapi.testclient import TestClient

from src.main import tracker


def test_answer():
    client = TestClient(app=tracker)
    result = client.get("/")
    assert result.status_code == 200
    assert result.json() == {"answer": "Success"}
