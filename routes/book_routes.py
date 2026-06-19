from fastapi import APIRouter, HTTPException
from database.book_db import book_db
from database.member_db import member_db
import services.book_service as service
import utils
from logs.config import logger

router = APIRouter()

@router.get('')
def get_all_books():
    books = book_db.get_all_books()
    if books:
        logger.info(f'return {len(books)} books')
    else:
        logger.warning('No books yet')
    return {'data': books}

@router.get('/{id}')
def get_book_by_id(id:int):
    book = book_db.get_book_by_id(id)
    if not book:
        raise HTTPException(404, 'Book not found')
    logger.info('return book')
    return {'data': book}

@router.post('', status_code=201)
def create_book(data:utils.BookModelCreating):
    logger.info('trying to create a new book...')
    id = service.create_book(book_db, data)
    logger.info(f'book created successfully, id = {id}')
    return {"msg": "book created successfully", 'data': {"id":id}}

@router.put('/{id}')
def update_book(id:int, data:utils.BookModelUpdating):
    book = book_db.get_book_by_id(id)
    if not book:
        raise HTTPException(404, 'Book not found')
    logger.info('try to update the book...')
    try:
        updated = service.update_book(book_db, id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    else:
        if not updated:
            raise HTTPException(400, 'Nothing updated')
        logger.info('Book updated successfully')
        return {"msg": "Book updated successfully"}


@router.put('/{id}/borrow{member_id}')
def borrow_book(id:int, member_id:int):
    try:
        service.borrow_book(book_db, member_db, id, member_id)
    except (utils.MemberNotFoundError, utils.BookNotFoundError) as e:
        raise HTTPException(404, e.detail)
    except ValueError as e:
        raise HTTPException(400, str(e))
    else:
        logger.info('Book borrowed successfully')
        return {"msg":"Book borrowed successfully"}

@router.put('/{id}/return/{member_id}')
def return_book(id:int, member_id:int):
    try:
        service.return_book(book_db, member_db, id, member_id)
    except (utils.MemberNotFoundError, utils.BookNotFoundError) as e:
        raise HTTPException(404, e.detail)
    except ValueError as e:
        raise HTTPException(400, str(e))
    else:
        logger.info('Book returned successfully')
        return {"msg":"Book returned successfully"}