# Nextのres.reqみたいな感じで、データを受け取る
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from uuid import uuid4
from sql.crud import createItem, getTableAllItems, getItemDetails

# Classを作成するためにBaseModelをインポート
from pydantic import BaseModel

app = FastAPI()
# 静的ファイルのディレクトリを指定
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
# テンプレートファイルのディレクトリを指定
templates = Jinja2Templates(directory="templates")
# engine = Engine
# Base.metadata.create_all(engine)
# DBsession = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
# session = DBsession()

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
# get(htmlレンダリング)処理
@app.get("/")
def root(
    skip: int = 0,
    limit: int = 10,
    completed: bool = False,
):
    # リダイレクト処理成功
    return RedirectResponse(f"/todo?skip={skip}&limit={limit}&completed={completed}")


# getエンドポイント
##########################################################################
@app.get(
    "/todo",
    response_class=HTMLResponse,
)
def mainPage(
    request: Request,
):
    todoLists = getTableAllItems("todoLists")
    todos = {
        "request": request,
        "todos": todoLists,
    }
    return templates.TemplateResponse("index.html", todos)


@app.get("/tag", response_class=HTMLResponse)
def tagPage(request: Request):
    tag = getTableAllItems("tags")
    tags = {"request": request, "tags": tag}
    return templates.TemplateResponse("tag.html", tags)


# Todo・タグ作成用のページ遷移用エンドポイント
##########################################################################
@app.get("/createTodo", response_class=HTMLResponse)
def createTodoPage(request: Request):
    tags = getTableAllItems("tags")
    if tags is None:
        alert = "タグが登録されていません"
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": alert}
        )
    return templates.TemplateResponse("createTodo.html", {"request": request})


@app.get("/createTagName", response_class=HTMLResponse)
def createTagPage(request: Request):

    return templates.TemplateResponse("createTag.html", {"request": request})


# 単体取得
##########################################################################
@app.get("/todo/{todoID}", response_class=JSONResponse)
def detail(request: Request, todoID: str):
    # ID検索をして一番最初のものを取得
    idCol = getItemDetails("relations", todoID)
    todo = {"request": request, "todo": idCol}
    return JSONResponse(todo)


@app.get("/tag/{tagID}", response_class=HTMLResponse)
def detail(request: Request, tagID: str):
    # ID検索をして一番最初のものを取得
    idCol = getItemDetails("tags", tagID)
    todo = {"request": request, "todo": idCol}
    return templates.TemplateResponse("detail.html", todo)


##########################################################################
# POST処理
@app.post("/todo", response_class=JSONResponse)
async def createTodo(request: Request):
    try:
        data = await request.json()
    except ValueError:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    createItem("todoLists", data)
    return JSONResponse(data)


@app.post("/tag", response_class=JSONResponse)
async def createTag(request: Request):
    try:
        data = await request.json()
        print(data)
        tagData = createItem("tags", data)
        # tagDataがCursorResult型の場合、適切な形式に変換する必要があります
        tagDataDict = tagData.all() if hasattr(tagData, "all") else tagData
        return JSONResponse(
            content={"message": "Tag created successfully", "tag": tagDataDict}
        )

    except ValueError:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)


# BASEファイル
##########################################################################
@app.get("/base", response_class=HTMLResponse)
def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", {"request": context})
