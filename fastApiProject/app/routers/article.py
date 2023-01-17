from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import app.cruds.article as dao
from app.admin.utils import current_time
from app.database import get_db

from app.schemas.article import ArticleDTO


router = APIRouter()

@router.post("/write", status_code=201)
async def write(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = dao.ArticleCrud(db)
    article = article_crud.find_article_by_userid(request_article=dto)
    if article is not None:
        result = article_crud.add_article(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="작성 불가"))
    return {"data": result}

@router.get("/read", status_code=201)
async def read(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = dao.ArticleCrud(db)
    article = article_crud.find_article_by_userid(request_article=dto)
    if article is not None:
        result = article_crud.read_article(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="열람 불가"))
    return result

@router.get("/read-all", status_code=201)
async def read_all(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = dao.ArticleCrud(db)

    if article_crud is not None:
        result = article_crud.read_all_articles(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="열람 불가"))
    return result

@router.put("/update", status_code=201)
async def update(dto: ArticleDTO, db: Session = Depends(get_db)):
    print(f"######### 수정을 시작한 시간: {current_time()} ")
    print(f"######### 수정글 정보 : {dto}")
    article_crud = dao.ArticleCrud(db)
    article = article_crud.find_article_by_userid(request_article=dto)
    if article is not None:
        print(f"내용 : {dto.content}")
        result = article_crud.update_article(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="작성 불가"))
    return {"data": result}

@router.delete("/delete", status_code=201)
async def delete(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = dao.ArticleCrud(db)
    print(f"###delete article crud: {article_crud}")
    article = article_crud.find_article_by_title(request_article=dto)
    print(f"###delete article: {article}")
    if article is not None:
        result = article_crud.delete_article(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="작성 불가"))
    return {"data": result}