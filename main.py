from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db_connection import ConnectionDB

@asynccontextmanager
async def lifespan(app:FastAPI):
    ConnectionDB.create_tables()
    print("Loading up the server")
    yield
    ConnectionDB.get_connection().close()
    print("Shutting down the server")

app = FastAPI(lifespan=lifespan)