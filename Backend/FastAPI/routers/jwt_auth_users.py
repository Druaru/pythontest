from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKE_DURATION = 1
SECRET = "1ad1ab6f3ef4c1cbca02294dacde1539"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])



class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDb(User):
    password: str

users_db = {
    "David" : {
        "username" : "David",
        "full_name" : "David Ruano Ruiz",
        "email": "davidruanoruiz@gmail.com",
        "disabled":False,
        "password": "$2a$12$dGpzw0PfCrLpcJdJgQPAyOv18bAmc2JD6u9IAPpRgLKCON/QzakYK"
    },
    "David2" : {
        "username" : "David2",
        "full_name" : "David Ruano Ruiz2",
        "email": "davidruanoruiz@gmail.com2",
        "disabled":True,
        "password": "$2a$12$n4XcMVaydoP3I8p3GUZBWuC131ke6SJQzDg5nbMoLzm77Gse8LxwG"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  
    

async def auth_user(token: str = Depends(oauth2)):
     
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})   

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
             raise exception

    except JWTError:
        raise  exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no escorrecta")

    access_token = {"sub":user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user