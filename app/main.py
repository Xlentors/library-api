from fastapi import FastAPI, HTTPException
from datetime import date, timedelta
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

class MemberCreate(BaseModel):
    name: str
    email: str

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class MemberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    
class LoanCreate(BaseModel):
    member_id: int
    book_id: int

class LoanResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    borrow_date: date
    due_date: date
    returned_date: date | None
    
    
# Data

books: list[dict] = []

members: list[dict] = []

loans: list[dict] = []
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

# MAIN

@app.get("/health")
def get_health():
    return {
        "status": "ok"
    }

# book endpoints
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

@app.get("/books/{book_id}", response_model=BookResponse)
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
        
# member endpoints
@app.get("/members", response_model=list[MemberResponse])
def get_members():
    return members

@app.post("/members", status_code=201, response_model=MemberResponse)
def create_member(member_create: MemberCreate):
    member_data = member_create.model_dump()
    member_data["id"] = get_next_member_id()
    member_data["is_active"] = True
    members.append(member_data)
    
    return member_data

@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    member = find_member(member_id)
    
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    return member

@app.patch("/members/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member_update: MemberUpdate):
    member = find_member(member_id)
        
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
        
    member_data = member_update.model_dump(exclude_none=True, exclude_unset=True)
    
    for key, val in member_data.items():
        member[key] = val
        
    return member

@app.delete("/members/{member_id}", response_model=MemberResponse)
def delete_member(member_id: int):
    member = find_member(member_id)
            
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    member["is_active"] = False
    
    return member
    
# loan endpoints
@app.post("/loans", status_code=201, response_model=LoanResponse)
def create_loan(loan_create: LoanCreate):
    member = find_member(loan_create.member_id)
    
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    book = find_book(loan_create.book_id)
        
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
        
    if not member["is_active"]:
        raise HTTPException(
            status_code=400,
            detail="Inactive member cannot borrow books"
        )
    
    if not book["is_active"]:
        raise HTTPException(
            status_code=400,
            detail="Inactive book cannot be borrowed"
        )

    if book["available_copies"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="No copies available"
        )
        
    active_loan_count = 0
    
    for loan in loans:
        if loan["member_id"] == loan_create.member_id and loan["returned_date"] is None:
            if loan["book_id"] == loan_create.book_id:
                raise HTTPException(
                    status_code=400,
                    detail="Member already has an active loan for this book"
                )
            
            active_loan_count += 1
            
    if active_loan_count >= 10:
        raise HTTPException(
            status_code=400,
            detail="Member has reached the active loan limit"
        )
        
    
    loan_data = loan_create.model_dump()
    loan_data["id"] = get_next_loan_id()
    loan_data["borrow_date"] = date.today()
    loan_data["due_date"] = loan_data["borrow_date"] + timedelta(days=21)
    loan_data["returned_date"] = None
    loans.append(loan_data)
    
    book["available_copies"] -= 1
    
    return loan_data
    
