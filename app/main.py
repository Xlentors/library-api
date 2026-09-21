from fastapi import FastAPI

from app.routers.books import router as books_router
from app.routers.members import router as members_router
from app.routers.loans import router as loans_router

app = FastAPI()
app.include_router(books_router)
app.include_router(members_router)
app.include_router(loans_router)

# MAIN

@app.get("/health")
def get_health():
    return {
        "status": "ok"
    }






