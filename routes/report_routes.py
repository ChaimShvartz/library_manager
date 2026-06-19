from fastapi import APIRouter
from database.book_db import book_db
from database.member_db import member_db
import services.reports_service as service
from logs.config import logger

router = APIRouter()

@router.get('/summary')
def get_summary() -> dict:
    summary = service.get_summary(book_db, member_db)
    logger.info('returns the summary')
    return summary

@router.get('/books-by-genre')
def get_books_by_genre() -> list[dict]:
    genres = ('Fiction', 'Non-Fiction', 'Science', 'History' ,'Other')
    books_by_genre = [{
        'Genre': genre,
        'COUNT': book_db.count_by_genre(genre)
        } for genre in genres]
    logger.info('returns books by genre')
    return books_by_genre

@router.get('/top_member')
def get_top_member() -> list[dict]:
    top_member = member_db.get_top_member()
    if top_member:
        logger.info(f'returns {len(top_member)} top members')
    else:
        logger.warning('No members yet')
    return top_member