from fastapi import FastAPI,Query,Depends,Request
# # from typing import Optional,list
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel,select
from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,Boolean
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session,load_only,session
import uvicorn
from fastapi import FastAPI, Body, Depends

from app.models.model import PostSchema, UserSchemasignup, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

# from sqlalchemy import select
# from sqlalchemy.sql import text

app=FastAPI()

users = []

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

#model
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    presents=Column(String,unique=True,index=True)
    absents=Column(String,unique=True,index=True)
    is_active=Column(Boolean,default=True)


#schema hero
class UserSchema(BaseModel):
    id:int
    presents:str
    absents:str
    is_active:bool

    class Config:
        orm_mode=True    

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close() 

Base.metadata.create_all(bind=engine)


@app.post("/users")
def index(user:UserSchema,db:Session=Depends(get_db)):
    u=User(presents=user.presents,absents=user.absents,is_active=user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchemasignup = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


# @app.post("/user/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         return signJWT(user.email)
#     return {
#         "error": "Wrong login details!"
#     }


@app.get("/show/",tags=["Show Data"])
def show_all_employees(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/presents",tags=["Show Data"])
def present_employees(db:Session = Depends(get_db)):
    users = db.query(User.presents).all()
    return users

@app.get("/absents",tags=["Show Data"])
def absent_employees(db:Session = Depends(get_db)):
    users = db.query(User.absents).all()
    return users




  




