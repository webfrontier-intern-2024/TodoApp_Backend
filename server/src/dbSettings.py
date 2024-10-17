from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

path = os.getenv("DB_PASS")

Engine = create_engine(path)


Base = declarative_base()


# ここでテーブルを作成する
class todoLists(Base):
    __tablename__ = "todolists"
    todoID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    taskName = Column(String(255), index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    finished = Column(Boolean, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)


class tags(Base):
    __tablename__ = "tags"
    tagID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    tagName = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)
