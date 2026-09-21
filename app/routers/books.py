from fastapi import APIRouter, HTTPException

from app.data import books
from app.helpers import find_book, get_next_book_id
from app.models import BookCreate, BookResponse, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])


@router.post("", status_code=201, response_model=BookResponse)
def create_book(book: BookCreate):
    book_data = book.model_dump()
    book_data["id"] = get_next_book_id()
    book_data["available_copies"] = book_data["total_copies"]
    book_data["is_active"] = True
    books.append(book_data)

    return book_data

@router.get("", response_model=list[BookResponse])
def get_books():
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = find_book(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book

@router.patch("/{book_id}", response_model=BookResponse)
def patch_book(book_id: int, book_update: BookUpdate):
    book = find_book(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book_data = book_update.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    if "total_copies" in book_data:
        new_total = book_data["total_copies"]

        borrowed_copies = book["total_copies"] - book["available_copies"]

        if new_total < borrowed_copies:
            raise HTTPException(
                status_code=400,
                detail="Total copies cannot be less than borrowed copies"
            )

        book["available_copies"] = new_total - borrowed_copies

    for key, val in book_data.items():
        book[key] = val

    return book

@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(book_id: int):
    book = find_book(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book["is_active"] = False

    return book