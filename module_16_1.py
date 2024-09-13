from fastapi import FastAPI
from fastapi import Query

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin():
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user(user_id: int):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user")
async def user_info(username: str = Query(...), age: int = Query(...)):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}