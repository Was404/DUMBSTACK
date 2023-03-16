from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
# впиши в браузере
# http://127.0.0.1:8000/docs
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Test FastAPI"
)

# Нужно создать точку входа куда клиенты смогут обращаться чтобы получать данны

test_users = [
    {"id": 1, "role": "team leader", "name": "ALEKSEI"},
    {"id": 2, "role": "backend developer", "name": "DANILA"},
    {"id": 3, "role": "backend developer", "name": "EGOR"},
    {"id": 4, "role": "backend developer", "name": "DIDYE", "degree": [
        {"id": 1, "created_at": "2023-03-03T00:00:00", "type_degree": "Master"}
    ]}
]


class DegreeType(Enum):
    newbie = "newbie"
    master = "Master"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[
        List[Degree]] = []  # Либо нам нужен этот список, либо не нужен. = [] просто пустой список если нету degree
    # параметр degree есть не у всех пользователей чтобы не было ошибок, юзаем


@app.get("/users/{user_id}", response_model=List[User])  # respons model - валидация того что мы отправляем на фронт
def get_user(user_id: int):
    return [user for user in test_users if user.get("id") == user_id]


test_passwd = [
    {"id": 1, "user_id": 1, "word": "ALEKSEI", "pass": 1234},
    {"id": 2, "user_id": 2, "word": "DANILA", "pass": 12345},
    {"id": 3, "user_id": 3, "word": "EGOR", "pass": 12346},
    {"id": 4, "user_id": 4, "word": "DIDYE", "pass": 12347}
]


@app.get("/users_pass")
def get_pass(limit: int,
             offset: int):  # откуда и до куда. также можно указать конкретные цифры int = 1, при запросе можно ничего не менять или вручную писать откуда до куда вернуть значения
    return test_passwd[offset:][limit:]  # Выводит с limit до offset список


test_users2 = [
    {"id": 1, "role": "team leader", "name": "ALEKSEI"},
    {"id": 2, "role": "backend developer", "name": "DANILA"},
    {"id": 3, "role": "backend developer", "name": "EGOR"},
    {"id": 4, "role": "backend developer", "name": "DIDYE"}
]


@app.post("/users/{user_id}")
def change_name(user_id: int, new_name: str):
    corrent_user = list(filter(lambda user: user.get("id") == user_id, test_users2))[
        0]  # фильтруем по полученному user id
    corrent_user["name"] = new_name
    return {"status": 200, "data": corrent_user}


#################ВАЛИДАЦИЯ ДАННЫХ##########################
class Trade(BaseModel):
    id: int
    parameter: int
    word: str = Field(max_length=10)  # максимум символов (в данном случае) 10
    values: int = Field(ge=0)  # обработчик, больше либо равно


test_somearray = [
    {"id": 1, "parameter": 32, "word": "SOMEWORDS", "values": 1245231},
    {"id": 2, "parameter": 15632, "word": "SOMEWORDS", "values": 1221}
]


@app.post("/trades")
def add_trades(trades: List[Trade]):
    test_somearray.extend(trades)
    return {"status": 200, "data": test_somearray}


# Выводит ошибки валидации (работает с response model)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


def hello():
    return "Hello world!"
# uvicorn main:app --reload
