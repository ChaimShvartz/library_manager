from mysql.connector.errors import IntegrityError
import utils
from logs.config import logger

def create_member(member_db, data:utils.MemberModelCreating):
    data = data.model_dump()
    try:
        return member_db.create_member(data)
    except IntegrityError:
        raise utils.EmailNotUniqueError

def update_member(member_db, id, data:utils.MemberModelUpdating):
    member = member_db.get_member_by_id(id)
    if not member:
        raise utils.MemberNotFoundError
    data = data.model_dump(exclude_unset=True)
    if not data:
        raise ValueError('nothing to update')
    logger.info('trying tp update the member...')
    try:
        return member_db.update_member(id, data)
    except IntegrityError:
        raise utils.EmailNotUniqueError

def deactivate_member(member_db, id):
    member = member_db.get_member_by_id(id)
    if not member:
        raise utils.MemberNotFoundError
    logger.info('trying to deactivate member...')
    return member_db.deactivate_member(id)

def activate_member(member_db, id):
    member = member_db.get_member_by_id(id)
    if not member:
        raise utils.MemberNotFoundError
    logger.info('trying to activate member...')
    return member_db.activate_member(id)
