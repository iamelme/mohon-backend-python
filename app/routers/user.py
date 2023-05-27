from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db
from ..utils import hash

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserIn])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


# creating a new user
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(add_user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"add user payload ", add_user)

    emailExist = db.query(models.User).filter(models.User.email == add_user.email).first()

    if emailExist:
        raise HTTPException(status_code=409, detail="This email alredy taken")

    hash_password = hash(add_user.password)
    add_user.password = hash_password

    new_user = models.User(**add_user.dict())
    print(f"new_user", new_user)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# update user
@router.put(
    "/{id}",
)
async def update_user(
    id: str,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    found_user = user_query.first()
    emailExist = db.query(models.User).filter(models.User.email == found_user.email).first()

    print("found_user type => ", type(found_user))
    print(f"user query", user.__dict__)

    if found_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")

    if emailExist and found_user.email != user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.email} already exist")

    if found_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are now allowed to update this user.",
        )

    user_query.update(user.dict(), synchronize_session=False)
    db.commit()

    return user.dict()


# deleting a user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str, db: Session = Depends(get_db), current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
):
    print(f"delete user id ", id)
    print(f"current_user", current_user)

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are now allowed to delete this user.",
        )

    print(f"delete user", user.__dict__)
    print(f"delete user is_active", user.is_active)

    user_query.update({"is_active": False}, synchronize_session=False)

    db.commit()

    return {}
