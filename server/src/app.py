from fastapi import FastAPI
import sqlalchemy

# Classを作成するためにBaseModelをインポート
from pydantic import BaseModel

app = FastAPI()


# Todoアイテムのデータ構造を定義
class Item(BaseModel):
    id: int
    title: str
    description: str = None
    finished: bool = False


@app.get("/")
def read_root():
    return {"Hello": "111"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# POST
@app.post("/create")
def create_item(item: Item):
    return {"item_name": item.title, "item_id": item.id}


# PUTの場合は、パスパラメータとリクエストボディの両方を受け取ることができる
@app.put("/change")
def update_item(item: Item):
    return {"item_name": item.title, "item_id": item.id}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=8001)
