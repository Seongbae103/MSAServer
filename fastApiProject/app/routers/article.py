from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, RedirectResponse

from app.cruds.article import ArticleCrud
from sqlalchemy.orm import Session
from app.schemas.article import ArticleDTO
from app.database import get_db

router = APIRouter()

@router.post("/register", status_code=201)
async def register_article(dto: ArticleDTO, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200,
                        content=dict(
                            msg=ArticleCrud(db).add_article(request_user=dto)))

@router.put("/modify", status_code=201)
async def modify_article(dto: ArticleDTO, db: Session = Depends(get_db)):
    if ArticleCrud(db).match_token(request_user=dto):
        return JSONResponse(status_code=200,
                            content=dict(
                                msg=ArticleCrud(db).update_article(dto)))
    else:
        RedirectResponse(url='/no-match-token', status_code=302)

@router.delete("/remove", status_code=201)
async def remove_article(dto: ArticleDTO, db: Session = Depends(get_db)):
    if ArticleCrud(db).match_token(request_user=dto):
        return JSONResponse(status_code=200,
                            content=dict(
                                msg=ArticleCrud(db).delete_user(dto)))
    else:
        RedirectResponse(url='/no-match-token', status_code=302)

@router.get("/page/{page}", status_code=201)
async def get_all_articles(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.find_all_articles(request_article=dto)

@router.get("/seq/{seq}", status_code=201)
async def get_article_by_seq(seq: int, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.find_article_by_seq(seq=seq)

@router.get("/id/{userid}/page/{page}", status_code=201)
async def get_articles_by_userid(userid:str, page:int, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.find_articles_by_userid(userid)

@router.get("/title/{title}/page/{page}", status_code=201)
async def get_articles_by_title(title:str, page:int, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.find_articles_by_title(title=title)


