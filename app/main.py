from fastapi import FastAPI
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

# Data

books: list[dict] = []

# Helpers

def get_next_book_id() -> int:
    highest_id = 0
    
    for book in books:
        highest_id = max(highest_id, book["id"])
        
    return highest_id + 1    

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


    