# from typing import Annotated
# from fastapi import APIRouter, Depends
# from app.core.security import get_current_user, verify_token_access
# from app.core.utils import assign_paging, common_params
# from app.curd import crud_pet
# from app.db.database import get_db
# from sqlalchemy.orm import Session

# from app.db.schemas.pet import create_pet_schema, update_pet_schema

# router = APIRouter()


# @router.get("/{pet_id}", dependencies=[Depends(get_current_user)])
# def get_pet(pet_id: int, session: Session = Depends(get_db)):
#     return crud_pet.get_pet(pet_id, session)


# @router.get("/", dependencies=[Depends(get_current_user)])
# def get_pets(
#     params: Annotated[dict, Depends(common_params)],
#     session: Session = Depends(get_db),
# ):
#     assign_paging(params)
#     return crud_pet.get_pets(session, params)


# @router.post("/", dependencies=[Depends(get_current_user)])
# def create_pet(pet: create_pet_schema, session: Session = Depends(get_db)):
#     return crud_pet.create_pet(session, pet)


# @router.put("/disable/{pet_id}", dependencies=[Depends(get_current_user)])
# def disable_pet(pet_id: int, session: Session = Depends(get_db)):
#     return crud_pet.disable_pet(session, pet_id)


# @router.put("/{pet_id}", dependencies=[Depends(get_current_user)])
# def update_pet(pet_id: int, pet: update_pet_schema, session: Session = Depends(get_db)):
#     return crud_pet.update_pet(session, pet_id, pet)
