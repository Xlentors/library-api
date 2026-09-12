# Library REST API

An in memory REST API for a library system built with Python, FastAPI, and Pydantic.

## Features
* Create, retreive, update, and deactive books and members
* Track book's availability
* Borrow and return books
* Track total and available book copies
* Return appropriate validation and not found errors
* Uses interactive API documentation via Swagger UI

## Tech Stack
* Python
* FastAPI
* Pydantic
* Uvicorn

# Enpoints
* Health: GET /health
* Books: POST /books, GET /books, GET /books/{book_id}, PATCH /books/{book_id}, DELETE /books/{book_id}
* Members: POST /members, GET /members, GET /members/{member_id}, PATCH /members/{member_id}, DELETE /members/{member_id}
* Loans: POST /loans, GET /loans/{loan_id}, PATCH /loans/{loan_id}/return

## How to Start
git clone https://github.com/Xlentors/library-api.git
cd library-api

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

fastapi dev app/main.py

Interactive documentation at:
http://127.0.0.1:8000/docs

## Current Scope
Currently the storage uses in-memory Python lists and resets when the server starts. This version mainly focuses on REST design, validation, and library rules (ex. loan limits or number of available books).