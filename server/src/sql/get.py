from sqlalchemy.orm import Session
from server.src.sql.dbSettings import SessionLocal, todoLists


def get_all_todo_items():
    # セッションを作成
    db: Session = SessionLocal()
    try:
        # すべてのTodoアイテムを取得
        todos = db.query(todoLists).all()
        return todos
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる
