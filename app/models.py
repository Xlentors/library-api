from datetime import date

from pydantic import BaseModel


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