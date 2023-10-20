from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Request

SQLALCHEMY_DB_URL='mysql+pymysql://root@localhost:3306/test'

engine=create_engine(SQLALCHEMY_DB_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

