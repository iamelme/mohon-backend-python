from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from ..utils import verify

router = APIRouter(tags=["Authentication"])


@router.post("/api/login", response_model=schemas.Token)
async def login(
    # user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
    user_cred: schemas.Login,
    db: Session = Depends(get_db),
):
    print(f"user_cred", user_cred)
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    print(f"user ", user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Email or/and password is incorrect",
        )

    if not verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email or/and password is incorrect",
        )

    print(f"user id ", user.id)

    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
