from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_existing_book():
    response = client.get("/books/1")
    assert response.status_code == 200

    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["title"] == "The Storm Before The Storm"

def test_get_missing_book():
    response = client.get("/books/991348")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_get_book_with_invalid_id():
    response = client.get("/books/test")
    assert response.status_code == 422