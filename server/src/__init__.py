from fastapi import FastAPI
from sqlalchemy import SQLAlchemy  # 追加

app = FastAPI(__name__)
app.config.from_object("fastapi.config")

db = SQLAlchemy(app)  # 追加
