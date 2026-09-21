from fastapi import APIRouter, HTTPException

from app.data import members
from app.helpers import find_member, get_next_member_id
from app.models import MemberCreate, MemberResponse, MemberUpdate


router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=list[MemberResponse])
def get_members():
    return members

@router.post("", status_code=201, response_model=MemberResponse)
def create_member(member_create: MemberCreate):
    member_data = member_create.model_dump()
    member_data["id"] = get_next_member_id()
    member_data["is_active"] = True
    members.append(member_data)

    return member_data

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    member = find_member(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member

@router.patch("/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member_update: MemberUpdate):
    member = find_member(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member_data = member_update.model_dump(exclude_none=True, exclude_unset=True)

    for key, val in member_data.items():
        member[key] = val

    return member

@router.delete("/{member_id}", response_model=MemberResponse)
def delete_member(member_id: int):
    member = find_member(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member["is_active"] = False

    return member