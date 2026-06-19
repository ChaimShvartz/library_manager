from pydantic import BaseModel
from typing import Literal

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

class MemberModelCreating(BaseModel):
    name: str
    email: str

class MemberModelUpdating(BaseModel):
    name: str | None = None
    email: str | None = None

class MemberNotFoundError(Exception):
    detail = "Member not found"

class EmailNotUniqueError(Exception):
    detail = "Email not unique"