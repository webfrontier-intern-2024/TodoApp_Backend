from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import MetaData, Table, insert, select
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sql.dbSettings import SessionLocal
from datetime import datetime


def getTableAllItems(tableName: str):
    # セッションを作成
    db: Session = SessionLocal()
    try:
        # メタデータを取得
        metadata = MetaData()
        # テーブルオブジェクトを取得
        table = Table(tableName, metadata, autoload_with=db.bind)
        # すべてのTodoアイテムを取得
        query = db.query(table)
        result = db.execute(query)
        items = result.fetchall()
        return items
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる


def getItemDetails(tableName: str, itemID: str):
    # セッションを作成
    db: Session = SessionLocal()
    try:
        # メタデータを取得
        metadata = MetaData()
        # テーブルオブジェクトを取得
        table = Table(tableName, metadata, autoload_with=db.bind)
        # すべてのTodoアイテムを取得
        query = db.query(table).filter(table.todoID == itemID).first()
        result = db.execute(query)
        item = result.fetchall()

        return item
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる


def createItem(tableName: str, data: dict):
    # セッションを作成
    if data is None:
        raise ValueError("Data must be a valid dictionary.")

    db: Session = SessionLocal()
    try:

        # メタデータを取得
        metadata = MetaData()
        # テーブルオブジェクトを取得
        table = Table(tableName, metadata, autoload_with=db.bind)

        # すべてのTodoアイテムを取得
        new_item = insert(table).values(**data)

        # db.refresh(new_item)
        return JSONResponse(content=new_item)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる
