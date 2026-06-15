from fastapi import APIRouter, HTTPException
from database.member_db import member_db
from services.member_service import *

router = APIRouter()

@router.get('')
def get_all_members():
    return member_db.get_all_members()

@router.get('/{id}')
def get_member_by_id(id:int):
    try:
        return get_member_by_id_service(member_db, id)
    except MemberNotFoundError as e:
        raise HTTPException(404, e.detail)

@router.post('', status_code=201)
def create_member(data:MemberModelCreating):
    try:
        id = create_member_srvice(member_db, data)
    except EmailNotUniqueError as e:
        raise HTTPException(409, e.detail)
    return {"id": id}

@router.put('/{id}')
def update_member(id:int, data:MemberModelUpdating):
    try:
        updated = update_member_service(member_db, id, data)
    except MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    except EmailNotUniqueError as e:
        raise HTTPException(409, e.detail)
    else:
        if updated:
            return {"msg":"Member updated successfully"}
        return {"msg":"Nothing updated"}

@router.put('/{id}/deactivate')
def deactivate_member(id:int):
    try:
        updating = deactivate_member_service(member_db, id)
    except MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    else:
        if updating:
            return {"msg":"Member deactivated successfully"}
        return {"msg":"Nothing updated"}

@router.put('/{id}/activate')
def activate_member(id:int):
    try:
        updating = activate_member_service(member_db, id)
    except MemberNotFoundError as e:
        raise HTTPException(404, e.detail)
    else:
        if updating:
            return {"msg":"Member activated successfully"}
        return {"msg":"Nothing updated"}