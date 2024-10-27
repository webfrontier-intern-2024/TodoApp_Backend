from sqlalchemy.orm import Session
from sql.dbSettings import SessionLocal, todoLists


def getTableItems(tableName: str):
    # セッションを作成
    db: Session = SessionLocal
    try:
        # すべてのTodoアイテムを取得
        todos = db.query(tableName).all()
        return todos
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる
