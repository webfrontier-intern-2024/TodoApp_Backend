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

        # select文を使用してアイテムを取得
        stmt = select(table).where(table.c[keyID] == searchID)
        result = db.execute(stmt).first()  # 最初の結果を取得

        return result  # Rowオブジェクトを返す
    except Exception as e:
        print(f"Error occurred: {e}")
        return None  # エラーが発生した場合はNoneを返す
    finally:
        db.close()


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

        # データを挿入
        # ISOフォーマットじゃないとエラーが出る
        data["created_at"] = datetime.now().isoformat(timespec="seconds")
        data["updated_at"] = datetime.now().isoformat(timespec="seconds")

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


def editData(tableName: str, data: dict, searchID: str, keyID: str):
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

        # データを挿入
        # ISOフォーマットじゃないとエラーが出る
        data["updated_at"] = datetime.now().isoformat(timespec="seconds")

        stmt = table.update().where(table.c[keyID] == searchID).values(**data)
        db.execute(stmt)
        db.commit()

        return {"message": "Item updated successfully"}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=400, detail="Error occurred while updating item."
        )
    finally:
        db.close()  # セッションを閉じる


def deleteData(tableName: str, searchID: str, keyID: str):
    # セッションを作成
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

        # データを削除
        stmt = table.delete().where(table.c[keyID] == searchID)
        db.execute(stmt)
        db.commit()

        return {"message": "Item deleted successfully"}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=400, detail="Error occurred while deleting item."
        )
    finally:
        db.close()  # セッションを閉じる
