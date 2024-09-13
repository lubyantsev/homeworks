from fastapi import FastAPI, Path, HTTPException
from typing import Dict, Annotated

app = FastAPI()

users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[
            str, Path(min_length=5, max_length=20, description="Введите имя пользователя", example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст", example=24)]
):
    new_id = str(max(map(int, users.keys()), default=0) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_id} is registered"}


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Введите ID пользователя", example=1)],
        username: Annotated[
            str, Path(min_length=5, max_length=20, description="Введите имя пользователя", example='UrbanProfi')],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст", example=28)]
):
    user_key = str(user_id)
    if user_key not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[user_key] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {user_id} has been updated"}


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Введите ID пользователя", example=2)]
):
    user_key = str(user_id)
    if user_key not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_key]
    return {"message": f"User {user_id} has been deleted"}
