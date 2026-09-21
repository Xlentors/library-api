from app.data import books, loans, members

def get_next_book_id() -> int:
    highest_id = 0

    for book in books:
        highest_id = max(highest_id, book["id"])

    return highest_id + 1

def find_book(book_id: int) -> dict | None:
    for book in books:
        if book["id"] == book_id:
            return book

    return None

def get_next_member_id() -> int:
    highest_id = 0

    for member in members:
        highest_id = max(highest_id, member["id"])

    return highest_id + 1

def find_member(member_id: int) -> dict | None:
    for member in members:
        if member["id"] == member_id:
            return member

    return None

def get_next_loan_id() -> int:
    highest_id = 0

    for loan in loans:
        highest_id = max(highest_id, loan["id"])

    return highest_id + 1

def find_loan(loan_id: int) -> dict | None:
    for loan in loans:
        if loan["id"] == loan_id:
            return loan

    return None