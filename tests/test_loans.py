from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.main import app, books, members, loans
from datetime import date, timedelta

client = TestClient(app)

INITIAL_BOOKS = deepcopy(books)
INITIAL_MEMBERS = deepcopy(members)
INITIAL_LOANS = deepcopy(loans)


@pytest.fixture(autouse=True)
def reset_data():
    books[:] = deepcopy(INITIAL_BOOKS)
    members[:] = deepcopy(INITIAL_MEMBERS)
    loans[:] = deepcopy(INITIAL_LOANS)


def test_create_loan_decreases_available_copies():
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 2, "book_id": 1},
    )

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["member_id"] == 2
    assert response_body["book_id"] == 1
    assert response_body["returned_date"] is None
    assert books[0]["available_copies"] == prev_available_copies - 1

def test_return_loan_increases_available_copies():
    prev_available_copies = books[0]["available_copies"]

    response = client.patch("/loans/1/return")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["returned_date"] == date.today().isoformat()
    assert books[0]["available_copies"] == prev_available_copies + 1

def test_duplicate_active_loan_is_rejected():
    prev_loan_count = len(loans)
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 1, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Member already has an active loan for this book"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == prev_available_copies

def test_loan_cannot_be_returned_twice():
    prev_available_copies = books[0]["available_copies"]
    response = client.patch("/loans/1/return")

    assert response.status_code == 200
    assert books[0]["available_copies"] == prev_available_copies + 1

    response = client.patch("/loans/1/return")

    assert response.status_code == 400
    assert response.json() == {"detail": "Loan has already been returned"}
    assert books[0]["available_copies"] == prev_available_copies + 1

def test_inactive_member_cannot_borrow():
    prev_loan_count = len(loans)
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 3, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive member cannot borrow books"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == prev_available_copies

def test_inactive_book_cannot_be_borrowed():
    books[0]["is_active"] = False
    prev_loan_count = len(loans)
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 2, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive book cannot be borrowed"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == prev_available_copies

def test_unavailable_book_cannot_be_borrowed():
    books[0]["available_copies"] = 0
    prev_loan_count = len(loans)

    response = client.post(
        "/loans",
        json={"member_id": 2, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "No copies available"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == 0

def test_member_cannot_exceed_active_loan_limit():
    for index in range(10):
        loans.append({
            "id": 100 + index,
            "member_id": 2,
            "book_id": 100 + index,
            "borrow_date": date.today(),
            "due_date": date.today() + timedelta(days=7),
            "returned_date": None,
        })

    prev_loan_count = len(loans)
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 2, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Member has reached the active loan limit"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == prev_available_copies

def test_member_with_overdue_loan_cannot_borrow():
    loans.append({
        "id": 200,
        "member_id": 2,
        "book_id": 200,
        "borrow_date": date.today() - timedelta(days=30),
        "due_date": date.today() - timedelta(days=1),
        "returned_date": None,
    })

    prev_loan_count = len(loans)
    prev_available_copies = books[0]["available_copies"]

    response = client.post(
        "/loans",
        json={"member_id": 2, "book_id": 1},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Member has an overdue loan"}
    assert len(loans) == prev_loan_count
    assert books[0]["available_copies"] == prev_available_copies