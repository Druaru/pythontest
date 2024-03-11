from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

router = APIRouter()

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id= 1, name = "David",surname = "Ruano",url = "https://DavRuvs.dev",age = 35),
        User(id= 2, name = "Luisillo",surname = "elPillo",url = "https://LuiPivs.dev",age= 25),
        User(id= 3, name = "Riki",surname = "Gaella",url = "https://RikiGavs.dev",age = 35)]
    
# ------------------------------------------GET----------------------------------------------------------

@router.get("/usersjson")
async def usersjson():
    return [{"name" : "David", "surname":"Ruano", "url":"https://DavRuvs.dev","edad":35},
            {"name" : "Luisillo", "surname":"elPillo", "url":"https://LuiPivs.dev","edad":25},
            {"name" : "Riki", "surname":"Gaella", "url":"https://RikiGavs.dev","edad":23}]


@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

 # Query   
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

    
# -----------------------------------------POST-------------------------------------------------------------
    
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(404, detail="El usuario ya existe")
    
    else:
        users_list.append(user)
        return user


# -----------------------------------------PUT--------------------------------------------------------------


@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"Error":"No se ha actualizado el usuario"}
        
    return user


# --------------------------------------DELETE--------------------------------------------------------------

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
        
    if not found:
        return {"error":"No se ha eliminado el usuario"}


# Function usada arriba
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se ha encontrado el usuario"}