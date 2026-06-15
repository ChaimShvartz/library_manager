from fastapi import APIRouter
from database.book_db import book_db
from database.member_db import member_db
from services.reports_service import *

router = APIRouter()

@router.get('/summary')
def get_summary() -> dict:
    return get_summary_service(book_db, member_db)

@router.get('/books-by-genre')
def get_books_by_genre() -> list[dict]:
    return book_db.count_by_genre()

@router.get('/top_member')
def get_top_member() -> list[dict]:
    return member_db.get_top_member()