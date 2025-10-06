from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI, Depends
from typing import Annotated

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"
engine = create_engine(sqlite_url)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app : FastAPI):
    SQLModel.metadata.create_all(engine)
    yield