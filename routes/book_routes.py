from fastapi import APIRouter, HTTPException
from database.book_db import book_db
from services.book_service import *
from services.member_service import get_member_by_id_service, MemberNotFoundError

router = APIRouter()

@router.get('')
def get_all_books():
    return book_db.get_all_books()

@router.get('/{id}')
def get_book_by_id(id:int):
    try:
        return get_book_by_id_service(book_db, id)
    except BookNotFoundError as e:
        raise HTTPException(404, e.detail)

@router.post('', status_code=201)
def create_book(data:BookModelCreating):
    id = create_book_service(book_db, data)
    return {"id":id}

@router.put('/{id}')
def update_book(id:int, data:BookModelUpdating):
    try:
        update_book_service(book_db, id, data)
    except BookNotFoundError as e:
        raise HTTPException(404, e.detail)
    else:
        return {"msg": "Book updated successfully"}

@router.put('/{id}/borrow{member_id}')
def borrow_book(id:int, member_id:int):
    try:
        member = get_member_by_id_service(member_id)
        borrow_book_service(book_db, member, id, member_id)
    except (MemberNotFoundError, BookNotFoundError) as e:
        raise HTTPException(404, e.detail)
    except ValueError as e:
        raise HTTPException(400, e.detail)
    else:
        return {"msg":"Book borrowed successfully"}

@router.put('/{id}/return/{member_id}')
def return_book(id:int, member_id:int):
    try:
        member = get_member_by_id_service(member_id)
        return_book_service(book_db, member, id, member_id)
    except (MemberNotFoundError, BookNotFoundError) as e:
        raise HTTPException(404, e.detail)
    except ValueError as e:
        raise HTTPException(400, e.detail)
    else:
        return {"msg":"Book returned successfully"}