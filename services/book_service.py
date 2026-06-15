from pydantic import BaseModel
from typing import Literal
from database.member_db import MemberDB

class BookModelCreating(BaseModel):
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'History', 'Other']

class BookModelUpdating(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Literal['Fiction', 'Non-Fiction',
                    'Science', 'History', 'Other'] | None = None   

class BookNotFoundError(Exception):
    detail = "Book not found"

def create_book_service(book_db, data:BookModelCreating):
    data = data.model_dump()
    id = book_db.create_book(data)
    return id

def update_book_service(book_db, id, data:BookModelUpdating):
    get_book_by_id_service(book_db, id)
    data = data.model_dump(exclude_unset=True)
    book_db.update_book(id, data)

def borrow_book_service(book_db, member, id, member_id):
    book = get_book_by_id_service(id)
    if not member['is_activate']:
        raise ValueError("Member is not active")
    if book['borrowed_by_member_id']:
        raise ValueError("Book is not available")
    if book_db.count_active_borrows_by_member(member_id) > 2:
        raise ValueError("Member has reached maximum borrows")
    book_db.set_availability(id, False, member_id)
    MemberDB.increment_borrows(member_id)

def return_book_service(book_db, member, id, member_id):
    book = get_book_by_id_service(id)
    if not member['is_activate']:
        raise ValueError("Member is not active")
    if not book['borrowed_by_member_id']:
        raise ValueError("Book is not borrowed")
    if book['borrow_by_member_id'] != member_id:
        raise ValueError("Book is not borrowed by this member")
    book_db.set_availability(id, True)

def get_book_by_id_service(book_db, id:int):
    book = book_db.get_book_by_id(id)
    if book:
        return book
    raise BookNotFoundError