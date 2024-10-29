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

    return RedirectResponse(f"/todo?skip={skip}&limit={limit}&completed={completed}")


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
    return templates.TemplateResponse(
        "createTodo.html", {"request": request, "tags": tags}
    )


@app.get("/createTagName", response_class=HTMLResponse)
def createTagPage(request: Request):
    return templates.TemplateResponse("createTag.html", {"request": request})


# getエンドポイント
##########################################################################
@app.get(
    "/todo",
    response_class=JSONResponse,
)
async def mainPage(request: Request):
    todoLists = getTableAllItems("todoLists")
    todos = {
        "request": request,
        "todos": todoLists,
    }
    print(todos)
    return templates.TemplateResponse("index.html", todos)


@app.get("/tag", response_class=JSONResponse)
def tagPage(request: Request):
    tag = getTableAllItems("tags")
    tags = {"request": request, "tags": tag}
    return templates.TemplateResponse("tag.html", tags)


##########################################################################
# POST処理
@app.post("/todo", response_class=JSONResponse)
async def createTodo(request: Request):
    try:
        data = await request.json()

        # 必要なフィールドが含まれているか確認
        if "taskName" not in data or "description" not in data or "tagID" not in data:
            return JSONResponse(
                {"error": "すべてのフィールドを入力してください"}, status_code=400
            )

        # createItemを呼び出す
        createTodo = createItem("todoLists", data)  # dataを渡す

        return JSONResponse(content=data)
    except ValueError:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)


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


# 単体取得
##########################################################################
@app.get("/todo/{todo_id}", response_class=JSONResponse)
def detail(request: Request, todo_id: str):
    # ID検索をして一番最初のものを取得
    idCol = getItemDetails("relations", todo_id, todo_id)
    todos = {"request": request, "todos": idCol}

    return templates.TemplateResponse("detail.html", todos)


@app.get("/tag/{tag_id}", response_class=JSONResponse)
async def detail(request: Request, tagID: str):
    # ID検索をして一番最初のものを取得
    idCol = getItemDetails("tags", tagID, tagID)
    tag = {"tags": idCol}
    jsonTags = JSONResponse(tag)
    return templates.TemplateResponse("tagDetail.html", jsonTags)


# BASEファイル
##########################################################################
@app.get("/base", response_class=HTMLResponse)
def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", {"request": context})
