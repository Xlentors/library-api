from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel

app = FastAPI()


# Classes

class BookCreate(BaseModel):
    title: str
    author: str
    date_published: date
    total_copies: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    date_published: date
    total_copies: int
    available_copies: int
    is_active: bool

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    date_published: date | None = None
    total_copies: int | None = None

# Data

books: list[dict] = []

# Helpers

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

# Main

@app.get("/health")
def get_health():
    return {
        "status": "ok"
    }

@app.post("/books", status_code=201, response_model=BookResponse)
def create_book(book: BookCreate):
    book_data = book.model_dump()
    book_data["id"] = get_next_book_id()
    book_data["available_copies"] = book_data["total_copies"]
    book_data["is_active"] = True
    books.append(book_data)
    
    return book_data

@app.get("/books", response_model=list[BookResponse])
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    return book

@app.patch("/books/{book_id}", response_model=BookResponse)
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
    
@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int):
    book = find_book(book_id)
    
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    book["is_active"] = False
    
    return book
        
        
    