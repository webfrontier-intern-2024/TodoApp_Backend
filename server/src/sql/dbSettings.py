from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UUID,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

path = os.getenv("DB_PASS")
Engine = create_engine(path)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


# ここでテーブルを作成する
# Modelsにすれば良かったかも


class todoLists(Base):
    __tablename__ = "todoLists"
    todoID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    taskName = Column(String(255), index=True, nullable=False)
    description = Column(Text, index=True, nullable=True)
    finished = Column(Boolean, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # settingsとのリレーションシップ
    relations = relationship("relations", back_populates="todoLists")


class tags(Base):
    __tablename__ = "tags"
    tagID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tagName = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # settingsとのリレーションシップ
    relations = relationship("relations", back_populates="tags")


class relations(Base):
    __tablename__ = "relations"
    settingID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    todoID = Column(
        UUID(as_uuid=True), ForeignKey("todoLists.todoID"), index=True, nullable=False
    )  # 外部キーを設定
    tagID = Column(
        Integer, ForeignKey("tags.tagID"), index=True, nullable=False
    )  # 外部キーを設定
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # リレーションシップの設定
    todo = relationship("todoLists", back_populates="relations")
    tag = relationship("tags", back_populates="relations")
