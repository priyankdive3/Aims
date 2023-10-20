from app.schemas.schemas import Employee
from fastapi import FastAPI, Body, Depends
from app.models.model import UserSchema, UserLoginSchema,UserSchemaIndex
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from fastapi import FastAPI,Depends, Body
from app.config.database import SessionLocal
from sqlalchemy.orm import Session
import uvicorn

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close() 

users = []

app = FastAPI()



def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

# route handlers

# testing
# @app.get("/", tags=["test"])
# def greet():
#     return {"hello": "world!."}



@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

@app.post("/users",tags=["Show Data"])
def index(user1:UserSchemaIndex,db:Session=Depends(get_db)):
    u=Employee(presents=user1.presents,absents=user1.absents,is_active=user1.is_active,id=user1.id)
    db.add(u)
    db.commit()
    return u

@app.get("/show/",tags=["Show Data"])
def show_all_employees(db:Session = Depends(get_db)):
    users = db.query(Employee).all()
    return users

@app.get("/presents",tags=["Show Data"])
def present_employees(db:Session = Depends(get_db)):
    users = db.query(Employee.presents).all()
    return users

@app.get("/absents",tags=["Show Data"])
def absent_employees(db:Session = Depends(get_db)):
    users = db.query(Employee.absents).all()
    return users