from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Создаем объект Jinja2Templates и указываем папку с шаблонами
templates = Jinja2Templates(directory="templates")

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Пустой список пользователей
users: List[User] = []

# Получение списка пользователей через корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def get_users_list(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Получение пользователя по ID
@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int = Path(..., description="Enter the user ID")):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

# Создание нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
async def create_user(
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", examples='UrbanUser'),
    age: int = Path(..., ge=18, le=120, description="Enter age", examples=24)
):
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# Обновление пользователя
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: int = Path(..., description="Enter the user ID", examples=1),
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", examples='UrbanProfi'),
    age: int = Path(..., ge=18, le=120, description="Enter age", examples=28)
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# Удаление пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: int = Path(..., description="Enter the user ID to delete", examples=2)
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
