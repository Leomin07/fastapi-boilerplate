# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy import and_, update
# from app.core.dict import CommonStatus
# from app.core.utils import return_paging
# from app.db import models
# from app.db.schemas import pet


# def check_pet_found(pet_id: int, db: Session):
#     pet = db.query(models.Pet).filter(
#         and_(models.Pet.id == pet_id, models.Pet.status == CommonStatus["ACTIVE"])
#     )
#     if pet is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found"
#         )

#     return True


# def get_pet(pet_id: int, db: Session):
#     pet = db.query(models.Pet).filter(
#         and_(models.Pet.id == pet_id, models.Pet.status == CommonStatus["ACTIVE"])
#     )
#     if pet is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found"
#         )

#     return pet


# def get_pets(db: Session, params: dict):
#     data = (
#         db.query(models.Pet)
#         .filter(models.Pet.status == CommonStatus["ACTIVE"])
#         .order_by(models.Pet.name.desc())
#         .limit(params["pageSize"])
#         .offset(params["skip"])
#         .all()
#     )
#     total_items = db.query(models.Pet).count()

#     return return_paging(data, total_items, params)


# def create_pet(db: Session, pet: pet.create_pet_schema):
#     data_pet = models.Pet(**pet.dict())
#     db.add(data_pet)
#     db.commit()
#     db.refresh(data_pet)
#     return pet


# def disable_pet(db: Session, pet_id: int):
#     check_pet_found(pet_id, db)
#     db.query(models.Pet).filter_by(id=pet_id).update(
#         {"status": CommonStatus["INACTIVE"]}
#     )
#     db.commit()


# def update_pet(db: Session, pet_id: int, item_in: pet.update_pet_schema):
#     check_pet_found(pet_id, db)

#     query = update(models.Pet).where(models.Pet.id == pet_id).values(**item_in.dict())
#     db.execute(query)
#     db.commit()
