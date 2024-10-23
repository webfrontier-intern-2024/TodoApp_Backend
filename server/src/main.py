# Nextのres.reqみたいな感じで、データを受け取る
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlalchemy
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import sessionmaker

from sql.dbSettings import Base, Engine

# Classを作成するためにBaseModelをインポート
from pydantic import BaseModel

app = FastAPI()
# 静的ファイルのディレクトリを指定
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
# テンプレートファイルのディレクトリを指定
templates = Jinja2Templates(directory="templates")
engine = Engine
Base.metadata.create_all(engine)
DBsession = SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
session = DBsession()

fake_todo_list = [
    {
        "id": uuid4(),
        "title": "買い物に行く",
        "description": "牛乳と卵を買う",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    },
    {
        "id": uuid4(),
        "title": "運動する",
        "description": "30分ジョギングする",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    },
]


# レスポンスの形式を設定する必要がある
@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/todo?skip={skip}&limit={limit}&completed={completed}")


@app.get(
    "/todo",
    response_class=HTMLResponse,
)
def mainPage(
    request: Request,
    skip=0,
    limit=10,
    completed=False,
):
    todos = {"request": request, "todos": fake_todo_list}
    return templates.TemplateResponse("index.html", todos)


@app.get("/todo/{todo_id}", response_class=HTMLResponse)
def detail(request: Request, todo_id: uuid4):
    todo = {"request": request, "todo": fake_todo_list[todo_id]}
    return templates.TemplateResponse("todo.html", todo)


@app.post("/todo", response_class=JSONResponse)
async def creatoeTodoItem(request: Request):

    data = await request.json()
    new_todo = {
        "id": uuid4(),
        "taskName": data["taskName"],
        "description": data["description"],
        "tags": data["tags"],
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }

    return JSONResponse(content=new_todo)


@app.get("todo/{todo_id}", response_class=HTMLResponse)
def get_todo_item(todo_id: int, request: Request):
    todo = {"request": request, "todo": fake_todo_list[todo_id]}
    return templates.TemplateResponse("todo.html", todo)


@app.get("/base", response_class=HTMLResponse)
def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", {"request": context})
