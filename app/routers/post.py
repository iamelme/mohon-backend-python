from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.get("/", response_model=schemas.PostOut)
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post)

    total = db.query(func.count(models.Post.id))

    if search:
        title_contains = models.Post.title.contains(search)
        posts = posts.filter(title_contains)
        total = total.filter(title_contains)

    posts = posts.limit(limit).offset(skip).all()

    total = total.scalar()
    return {"data": posts, "skip": skip, "limit": limit, "total": total}


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find id of {id}")
    return post


# adding post
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def new_post(
    add_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user),
):
    print(add_post)
    test = add_post.dict()
    print(f"test{test}")

    print(f"current_user", current_user)
    new_post = models.Post(user_id=current_user.id, **add_post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# deleting post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: str,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot find id of  the quick brown fox jumps over the lazy dog.{id}",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are now allowed to delete this post.",
        )

    # conn.commit()
    post_query.delete()

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating post
@router.put("/{id}")
async def update_post(
    id: str,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    found_post = post_query.first()

    # print(post)
    # print(post.dict())
    # print(f"is the same?", found_post.user_id == current_user.id)
    # print(found_post.user_id, current_user.id)
    # print("after post first")

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find id {id}")

    if found_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this post.",
        )
    # conn.commit()

    print(post.dict())
    print("after post.dict()")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return {"data": "done"}
