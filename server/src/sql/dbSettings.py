from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID, ForeignKey
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
class todoLists(Base):
    __tablename__ = "todolists"
    todoID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    taskName = Column(String(255), index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    finished = Column(Boolean, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # settingsとのリレーションシップ
    settings = relationship("settings", back_populates="todoLists")


class tags(Base):
    __tablename__ = "tags"
    tagID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    tagName = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # settingsとのリレーションシップ
    settings = relationship("settings", back_populates="tags")


class settings(Base):
    __tablename__ = "settings"
    settingID = Column(UUID(as_uuid=True), primary_key=True, index=True)
    todoID = Column(
        UUID(as_uuid=True), ForeignKey("todolists.todoID"), index=True, nullable=False
    )  # 外部キーを設定
    tagID = Column(
        UUID(as_uuid=True), ForeignKey("tags.tagID"), index=True, nullable=False
    )  # 外部キーを設定
    created_at = Column(DateTime, index=True, nullable=False)
    updated_at = Column(DateTime, index=True, nullable=False)

    # リレーションシップの設定
    todo = relationship("todoLists", back_populates="settings")
    tag = relationship("tags", back_populates="settings")
