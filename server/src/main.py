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
from sql.get import getAllTodoItems

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
        "todoID": uuid4(),
        "taskName": "買い物に行く",
        "description": "牛乳と卵を買う",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    },
    {
        "todoID": uuid4(),
        "taskName": "運動する",
        "description": "30分ジョギングする",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    },
]


# レスポンスの形式を設定する必要がある
# get処理
@app.get("/", response_class=HTMLResponse)
def root(
    skip: int = 0,
    limit: int = 10,
    completed: bool = False,
):
    # リダイレクト処理成功
    return RedirectResponse(f"/todo?skip={skip}&limit={limit}&completed={completed}")


@app.get(
    "/todo",
    response_class=HTMLResponse,
)
def mainPage(
    request: Request,
):
    todos = {
        "request": request,
        "todos": fake_todo_list,
    }
    return templates.TemplateResponse("index.html", todos)


@app.get("/todo/{todoID}", response_class=HTMLResponse)
def detail(request: Request, todoID: uuid4):

    todo = {"request": request, "todo": fake_todo_list}
    return templates.TemplateResponse("todo.html", todo)


# Todo作成用のページ遷移用エンドポイント
@app.get("/createTodo", response_class=HTMLResponse)
def createTodoPage(request: Request):
    return templates.TemplateResponse("createTodo.html", {"request": request})


@app.get("/createTag", response_class=HTMLResponse)
def createTagPage(request: Request):
    return templates.TemplateResponse("createTag.html", {"request": request})


# POST処理
@app.post("/todo", response_class=JSONResponse)
async def creatoeTodoItem(request: Request):
    data = await request.json()
    new_todo = {
        "todoID": uuid4(),
        "taskName": data["taskName"],
        "description": data["description"],
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }

    return JSONResponse(content=new_todo)


# BASEファイル
##########################################
@app.get("/base", response_class=HTMLResponse)
def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", {"request": context})
