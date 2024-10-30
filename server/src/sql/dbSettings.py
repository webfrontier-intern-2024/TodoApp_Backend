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
import sqlalchemy as sa
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
    finished = Column(Boolean, index=True, nullable=False, default=False)
    limit_at = Column(DateTime, index=True, nullable=True)
    created_at = Column(DateTime, index=True, nullable=True, default=sa.func.now())
    updated_at = Column(DateTime, index=True, nullable=True, onupdate=sa.func.now())

    # tagsテーブルからの外部キー
    tagID = Column(
        UUID(as_uuid=True), ForeignKey("tags.tagID"), index=True, nullable=True
    )  # 外部キーを追加

    # settingsとのリレーションシップ
    tags = relationship("tags", back_populates="todoLists")  # リレーションシップを追加


class tags(Base):
    __tablename__ = "tags"
    tagID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    tagName = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=True, default=sa.func.now())
    updated_at = Column(DateTime, index=True, nullable=True, onupdate=sa.func.now())

    # todoListsとのリレーションシップ
    todoLists = relationship(
        "todoLists", back_populates="tags"
    )  # リレーションシップを追加
