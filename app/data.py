from datetime import date, timedelta

books: list[dict] = [
    {
        "id": 1,
        "title": "The Storm Before The Storm",
        "author": "Mike Duncan",
        "date_published": date(2017, 10, 24),
        "total_copies": 3,
        "available_copies": 2,
        "is_active": True,
    },
    {
        "id": 2,
        "title": "Cyberpunk 2077: No Coincidence",
        "author": "Rafał Kosik",
        "date_published": date(2023, 8, 23),
        "total_copies": 2,
        "available_copies": 1,
        "is_active": True,
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "date_published": date(1949, 6, 8),
        "total_copies": 1,
        "available_copies": 1,
        "is_active": True,
    },
]

members: list[dict] = [
    {
        "id": 1,
        "name": "Alex Reader",
        "email": "alex@example.com",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Jordan Lee",
        "email": "jordan@example.com",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Marcus Aurelius",
        "email": "marcus@example.com",
        "is_active": False,
    },
]

loans: list[dict] = [
    {
        "id": 1,
        "member_id": 1,
        "book_id": 1,
        "borrow_date": date.today() - timedelta(days=5),
        "due_date": date.today() + timedelta(days=16),
        "returned_date": None,
    },
    {
        "id": 2,
        "member_id": 1,
        "book_id": 2,
        "borrow_date": date.today() - timedelta(days=30),
        "due_date": date.today() - timedelta(days=9),
        "returned_date": None,
    },
    {
        "id": 3,
        "member_id": 2,
        "book_id": 3,
        "borrow_date": date.today() - timedelta(days=40),
        "due_date": date.today() - timedelta(days=19),
        "returned_date": date.today() - timedelta(days=25),
    },
]