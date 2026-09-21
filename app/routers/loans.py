from datetime import date, timedelta

from fastapi import APIRouter, HTTPException

from app.data import loans
from app.helpers import find_book, find_loan, find_member, get_next_loan_id
from app.models import LoanCreate, LoanResponse


router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("", status_code=201, response_model=LoanResponse)
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
            if loan["due_date"] < date.today():
                raise HTTPException(
                    status_code=400,
                    detail="Member has an overdue loan"
                )

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

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int):
    loan = find_loan(loan_id)

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    return loan

@router.patch("/{loan_id}/return", response_model=LoanResponse)
def return_loan(loan_id: int):
    loan = find_loan(loan_id)

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    if loan["returned_date"] is not None:
        raise HTTPException(
            status_code=400,
            detail="Loan has already been returned"
        )


    book = find_book(loan["book_id"])

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    loan["returned_date"] = date.today()
    book["available_copies"] += 1
    return loan

@router.get("", response_model=list[LoanResponse])
def get_loans(
    member_id: int | None = None,
    book_id: int | None = None,
    active: bool | None = None,
):
    res = []

    for loan in loans:
        member_matches = member_id is None or loan["member_id"] == member_id
        book_matches = book_id is None or loan["book_id"] == book_id

        if active is None:
            active_matches = True
        elif active:
            active_matches = loan["returned_date"] is None
        else:
            active_matches = loan["returned_date"] is not None

        if book_matches and member_matches and active_matches:
            res.append(loan)


    return res