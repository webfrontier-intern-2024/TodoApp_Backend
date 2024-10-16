from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.dbSettings import Base

# これ怪しい


class TodoItem(Base):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    finished = Column(Boolean, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)

    def __repr__(self):
        return f"<todo_items(id={self.id}, title={self.title}, description={self.description}, finished={self.finished}, created_at={self.created_at}, updated_at={self.updated_at})>"
