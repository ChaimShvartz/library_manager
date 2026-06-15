from pydantic import BaseModel
from mysql.connector.errors import IntegrityError

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

def get_member_by_id_service(member_db, id:int):
    member = member_db.get_by_id(id)
    if member:
        return member
    raise MemberNotFoundError

def create_member_srvice(member_db, data:MemberModelCreating):
    data = data.model_dump()
    try:
        return member_db.create_member(data)
    except IntegrityError:
        raise EmailNotUniqueError

def update_member_service(member_db, id, data:MemberModelUpdating):
    get_member_by_id_service(member_db, id)
    data = data.model_dump(exclude_unset=True)
    if not data:
        return False
    try:
        member_db.update_member(id, data)
    except IntegrityError:
        raise EmailNotUniqueError
    else:
        return True

def deactivate_member_service(member_db, id):
    get_member_by_id_service(member_db, id)
    return member_db.deactivate_member(id)

def activate_member_service(member_db, id):
    get_member_by_id_service(member_db, id)
    return member_db.activate_member(id)
