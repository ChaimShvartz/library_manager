from fastapi import APIRouter, HTTPException
from database.member_db import member_db
import services.member_service as service
import utils
from logs.config import logger

router = APIRouter()

@router.get('')
def get_all_members():
    members = member_db.get_all_members()
    if members:
        logger.info(f'returns {len(members)} members')
    else:
        logger.warning('No members yet')
    return {'data': members}

@router.get('/{id}')
def get_member_by_id(id:int):
    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(404, 'Member not found')
    logger.info('returns the member')
    return {'data': member}

@router.post('', status_code=201)
def create_member(data:utils.MemberModelCreating):
    logger.info('trying to create a new member...')
    try:
        id = service.create_member(member_db, data)
    except utils.EmailNotUniqueError as e:
        raise HTTPException(409, e.detail)
    logger.info(f'Member created successfully, id = {id}')
    return {'msg': 'Member created successfully', 'data': {"id": id}}

@router.put('/{id}')
def update_member(id:int, data:utils.MemberModelUpdating):
    try:
        updated = service.update_member(member_db, id, data)
    except utils.MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    except utils.EmailNotUniqueError as e:
        raise HTTPException(409, e.detail)
    except ValueError as e:
        raise HTTPException(400, str(e))
    else:
        if not updated:
            raise HTTPException(400, 'Nothing updated')    
        logger.info('Member updated successfully')
        return {"msg":"Member updated successfully"}

@router.put('/{id}/deactivate')
def deactivate_member(id:int):
    try:
        updating = service.deactivate_member(member_db, id)
    except utils.MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    else:
        if not updating:
            raise HTTPException(400, 'member already inactive')
        logger.info('Member deactivated successfully')
        return {"msg":"Member deactivated successfully"}

@router.put('/{id}/activate')
def activate_member(id:int):
    try:
        updating = service.activate_member(member_db, id)
    except utils.MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    else:
        if not updating:
            raise HTTPException(400, 'member already active')
        logger.info('Member activated successfully')
        return {"msg":"Member activated successfully"}