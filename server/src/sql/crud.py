from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import MetaData, Table, insert, select
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sql.dbSettings import SessionLocal
from datetime import datetime, timezone


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


def getItemDetails(tableName: str, keyID: str, searchID: str):
    # セッションを作成
    db: Session = SessionLocal()
    try:
        # メタデータを取得
        metadata = MetaData()
        # テーブルオブジェクトを取得
        table = Table(tableName, metadata, autoload_with=db.bind)
        # すべてのTodoアイテムを取得
        query = db.query(table).filter(table.keyID == searchID).first()
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
        table = Table(
            tableName,
            metadata,
            autoload_with=db.bind,
        )

        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()

        stmt = insert(table).values(**data)
        new_item = db.execute(stmt)
        db.commit()

        return new_item.inserted_primary_key_rows

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=400, detail="Error occurred while creating item."
        )
    finally:
        db.close()  # セッションを閉じる
