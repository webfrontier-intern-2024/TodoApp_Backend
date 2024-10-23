from sqlalchemy.orm import Session
from dbSettings import todoLists, tags, settings
from sqlalchemy.exc import DBAPIError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException


def getTodos(db: Session):
    todoObj = db.query(todoLists).all()
    try:
        Session.add(todoObj)
    except DBAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    Session.commit()
    Session.refresh(todoObj)
    return todoObj


def getTags(db: Session):
    tagObj = db.query(tags).all()
    try:
        Session.add(tagObj)
    except DBAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    Session.commit()
    Session.refresh(tagObj)
    return tagObj
