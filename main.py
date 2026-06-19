from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database.db_connection import db
from routes.book_routes import router as books_router
from routes.member_routes import router as members_router
from routes.report_routes import router as reports_router
from logs.config import logger

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info('Loading up the server')
    db.create_database()
    db.create_tables()
    yield
    db.close()
    logger.info('Shutting down the server')

app = FastAPI(lifespan=lifespan)

@app.middleware('HTTP')
def middleware(req:Request, next):
    logger.info(f'{req.url.path} - {req.method}')
    return next(req)

@app.exception_handler(HTTPException)
def handle_exception(req, e:HTTPException):
    logger.warning(e.detail)
    return JSONResponse({'detail': e.detail}, e.status_code)

app.include_router(books_router, prefix='/books', tags=['Books'])
app.include_router(members_router, prefix='/members', tags=['Members'])
app.include_router(reports_router, prefix='/reports', tags=['Reports'])