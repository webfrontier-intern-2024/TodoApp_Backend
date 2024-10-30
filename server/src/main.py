# Nextのres.reqみたいな感じで、データを受け取る
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from uuid import uuid4
from sql.crud import createItem, getTableAllItems, getItemDetails, editData, deleteData

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


# レスポンスの形式を設定する必要がある
# get(htmlレンダリング)処理
@app.get("/")
def root(
    skip: int = 0,
    limit: int = 10,
    completed: bool = False,
):

    return RedirectResponse(f"/todo?skip={skip}&limit={limit}&completed={completed}")


# Todo・タグ作成などののページ遷移用エンドポイント
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


@app.get("/editTag", response_class=JSONResponse)
def editTagPage(request: Request):

    return templates.TemplateResponse("editTag.html", {"request": request})


@app.get("/editTodo", response_class=JSONResponse)
def editTodoPage(request: Request):
    tag = getTableAllItems("tags")

    return templates.TemplateResponse(
        "editTodo.html", {"request": request, "tags": tag}
    )


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

    return templates.TemplateResponse("index.html", todos)


@app.get("/tag", response_class=JSONResponse)
async def tagPage(request: Request):
    tag = getTableAllItems("tags")
    tags = {"request": request, "tags": tag}
    return templates.TemplateResponse("tag.html", tags)


# 単体取得
##########################################################################
@app.get("/todo/{todo_id}", response_class=JSONResponse)
async def detail(request: Request, todo_id: str):
    idCol = getItemDetails("todoLists", "todoID", todo_id)
    todo = {"request": request, "todo": idCol}

    return templates.TemplateResponse("todoDetail.html", todo)


@app.get("/tag/{tag_id}", response_class=JSONResponse)
async def detail(request: Request, tag_id: str):
    idCol = getItemDetails("tags", "tagID", tag_id)
    tag = {"request": request, "tag": idCol}
    return templates.TemplateResponse("tagDetail.html", tag)


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
        createItem("todoLists", data)  # dataを渡す

        return JSONResponse(
            content={"message": "Tag created successfully", "tag": data},
        )
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


# PUT
##########################################################################
@app.put("/todo/{todo_id}", response_class=JSONResponse)
async def updateTodo(request: Request, todo_id: str):
    req = await request.json()
    editTodo = editData("todoLists", req, todo_id, "todoID")
    return JSONResponse(
        content={
            "message": f"Update todo item with ID {todo_id}",
            "todo": editTodo,
        }
    )


@app.put("/tag/{tag_id}", response_class=JSONResponse)
async def updateTag(request: Request, tag_id: str):
    req = await request.json()

    editTag = editData("tags", req, tag_id, "tagID")

    return JSONResponse(
        content={
            "message": f"Update tag item with ID {tag_id}",
            "tag": editTag,
        }
    )


# DELETE
##########################################################################
@app.delete("/todo/{todo_id}", response_class=JSONResponse)
async def deleteTodo(request: Request, todo_id: str):
    delTodo = await request.json()
    deleteData("todoLists", todo_id, "todoID")

    return JSONResponse(
        content={
            "message": f"Delete todo item with ID {todo_id}",
            "todo": delTodo,
        }
    )


@app.delete("/tag/{tag_id}", response_class=JSONResponse)
async def deleteTag(request: Request, tag_id: str):

    delReq = await request.json()
    deleteData("todoLists", tag_id, "tagID")
    deleteData("tags", tag_id, "tagID")

    return JSONResponse(
        content={"message": f"Deleted tag with ID {tag_id}.", "tag": delReq}
    )
