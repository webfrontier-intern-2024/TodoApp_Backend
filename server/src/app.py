from fastapi import FastAPI
import sqlalchemy
import datetime
import uuid

# Classを作成するためにBaseModelをインポート
from pydantic import BaseModel

app = FastAPI()


# Todoアイテムのデータ構造を定義
class todoLists(BaseModel):
    todoID: uuid.UUID
    taskName: str
    description: str = None
    finished: bool = False
    createdAt: datetime
    updatedAt: datetime


class tags(BaseModel):
    tagID: uuid.UUID
    tagName: str
    createdAt: datetime
    updatedAt: datetime


class settings(BaseModel):
    settingID: uuid.UUID
    todoID: uuid.UUID
    tagID: uuid.UUID
    createdAt: datetime
    updatedAt: datetime


@app.get("/")
def read_root():
    return {"Hello": "111"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# POST
@app.post("/create")
def create_item(item: todoLists):
    return {"item_name": item.title, "item_id": item.id}


# PUTの場合は、パスパラメータとリクエストボディの両方を受け取ることができる
@app.put("/change")
def update_item(item: todoLists):
    return {"item_name": item.title, "item_id": item.id}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id}
