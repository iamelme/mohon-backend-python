from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

from ..utils import hash

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserIn])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


# creating a new user
@router.post(
    "/new", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
async def create_user(add_user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"add user payload ", add_user)

    emailExist = (
        db.query(models.User).filter(models.User.email == add_user.email).first()
    )

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
