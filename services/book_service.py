import utils
from logs.config import logger
def create_book(book_db, data:utils.BookModelCreating):
    data = data.model_dump()
    id = book_db.create_book(data)
    return id

def update_book(book_db, id,  data:utils.BookModelUpdating):
    data = data.model_dump(exclude_unset=True)
    if not data:
        raise ValueError('nothing to update')
    return book_db.update_book(id, data)

def borrow_book(book_db, member_db, book_id, member_id):
    member = member_db.get_member_by_id(member_id)
    if not member:
        raise utils.MemberNotFoundError
    book = book_db.get_book_by_id(book_id)
    if not book:
        raise utils.BookNotFoundError
    logger.info('try to borrow the book...')
    if not member['is_active']:
        raise ValueError("Member is not active")
    if book['borrowed_by_member_id']:
        raise ValueError("Book is not available")
    if book_db.count_active_borrows_by_member(member_id) >= 3:
        raise ValueError("Member has reached maximum borrows")
    book_db.set_availability(book_id, False, member_id)
    member_db.increment_borrows(member_id)

def return_book(book_db, member_db, book_id, member_id):
    member = member_db.get_member_by_id(member_id)
    if not member:
        raise utils.MemberNotFoundError
    book = book_db.get_book_by_id(book_id)
    if not book:
        raise utils.BookNotFoundError
    logger.info('try to return the book...')
    if not book['borrowed_by_member_id']:
        raise ValueError("Book is not borrowed")
    if book['borrowed_by_member_id'] != member_id:
        raise ValueError("Book is not borrowed by this member")
    book_db.set_availability(book_id, True)
