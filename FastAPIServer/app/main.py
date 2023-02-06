import uvicorn
from fastapi_pagination import add_pagination
global API_TOKEN, router, app
import os
import sys
import logging
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.responses import HTMLResponse
from .admin.utils import current_time
from .env import DB_URL
from app.database import init_db
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from .routers.user import router as user_router
from .routers.article import router as article_router  # 해당 경로에 있는 APIrouter()와 파일명이 합쳐져서 만들어짐
from .admin.pagination import router as pagination_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader


API_TOKEN = "SECRET_API_TOKEN"
api_key_header = APIKeyHeader(name="Token")
print(f" ################ app.main Started At {current_time()} ################# ")
router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(article_router, prefix="/articles", tags=["articles"])
router.include_router(pagination_router, prefix="/pagination", tags=["pagination"])
app = FastAPI()
add_pagination(app)
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.router.redirect_slashes = False
app.include_router(router)
app.add_middleware(DBSessionMiddleware, db_url=DB_URL)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

@app.get("/")
async def home():
    return HTMLResponse(content=f"""
    <body>
    <div>
        <h1 style="width:400px;margin:50px auto">
            {current_time()} <br/>
            현재 서버 구동 중 입니다. 
         </h1>
    </div>
    </body>
        """)

@app.get("/protected-router")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=403)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/no-match-token")
async def no_match_token():
    return {"message": f"토큰 유효시간이 지났습니다."}

 # handler = Mangum(app) 아마존에서 쓴다