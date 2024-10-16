from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

path = "postgresql://user:password@localhost:5432/mydatabase"

Engine = create_engine(path)

Base = declarative_base()
