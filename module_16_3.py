from fastapi import FastAPI, Path
from typing import Dict

app = FastAPI()

users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", example='UrbanUser'),
    age: int = Path(..., ge=18, le=120, description="Enter age", example=24)
):
    user_id = str(max(map(int, users.keys())) + 1) if users else '1'
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: str = Path(..., description="Enter the user ID", example='1'),
    username: str = Path(..., min_length=5, max_length=20, description="Enter username", example='UrbanProfi'),
    age: int = Path(..., ge=18, le=120, description="Enter age", example=28)
):
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id} has been updated"
    return f"User {user_id} does not exist"

@app.delete("/user/{user_id}")
async def delete_user(
    user_id: str = Path(..., description="Enter the user ID to delete", example='2')
):
    if user_id in users:
        del users[user_id]
        return f"User {user_id} has been deleted"
    return f"User {user_id} does not exist"
