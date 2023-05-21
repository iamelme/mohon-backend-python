from fastapi import FastAPI

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from datetime import datetime

import uuid

from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import auth, post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# # connect to database
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="mohon",
#             user="postgres",
#             password="",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("===== Database connected!. =====")
#         break
#     except Exception as error:
#         print("Cannot connect to database!.", error)
#         time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# retrieving
@app.get("/")
async def root():
    return {"message": "Hello World reload"}
