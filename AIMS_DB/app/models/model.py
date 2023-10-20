from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column,String,Integer,Boolean
from app.config.database import Base
#user signup
class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }
#user login
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }



#model
class UserSchemaIndex(BaseModel):
    id:int
    presents:str
    absents:str
    is_active:bool

class Check(Base):
    __tablename__="check"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True)
    is_active=Column(Boolean)

class CheckSchema(BaseModel):
    id:int
    name:str
    is_active:bool    

