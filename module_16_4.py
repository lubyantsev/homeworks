from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Пустой список пользователей
users: List[User] = []

# Получение списка пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users

# Создание нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
async def create_user(
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", example='UrbanUser'),
    age: int = Path(..., ge=18, le=120, description="Enter age", example=24)
):
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# Обновление пользователя
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: int = Path(..., description="Enter the user ID", example=1),
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", example='UrbanProfi'),
    age: int = Path(..., ge=18, le=120, description="Enter age", example=28)
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
    user_id: int = Path(..., description="Enter the user ID to delete", example=2)
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
