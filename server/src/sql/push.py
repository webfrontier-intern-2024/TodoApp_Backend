from sqlalchemy.orm import Session
from server.src.sql.dbSettings import SessionLocal, todoLists
from datetime import datetime
import uuid


def create_todo_item(task_name: str, description: str):
    # セッションを作成
    db: Session = SessionLocal()
    try:
        # 新しいTodoアイテムを作成
        new_todo = todoLists(
            todoID=uuid.uuid4(),  # 新しいUUIDを生成
            taskName=task_name,
            description=description,
            finished=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # データベースに追加
        db.add(new_todo)
        db.commit()  # 変更をコミット
        db.refresh(new_todo)  # 新しいアイテムをリフレッシュ
        return new_todo
    except Exception as e:
        db.rollback()  # エラーが発生した場合はロールバック
        print(f"Error occurred: {e}")
    finally:
        db.close()  # セッションを閉じる
