from sqlalchemy import Column,String,Integer,Boolean
from app.config.database import Base
#schema
class Employee(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    presents=Column(String,unique=True,index=True)
    absents=Column(String,unique=True,index=True)
    is_active=Column(Boolean,default=True)