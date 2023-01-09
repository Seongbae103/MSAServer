import os
import sys
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI, APIRouter
from app.env import DB_URL
from app.routers.user import router as user_router
from app.routers.post import router as post_router

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])     #경로지정 : APIRouter().include-router(import한 router, prefix="경로", tags=["table명"])
router.include_router(post_router, prefix="/posts", tags=["posts"])
app = FastAPI()
app.include_router(router)
app.add_middleware(DBSessionMiddleware, db_url=DB_URL)

@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
