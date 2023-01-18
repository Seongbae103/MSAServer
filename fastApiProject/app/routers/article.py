from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.cruds.article import ArticleCrud
from app.database import get_db
from app.schemas.article import ArticleDTO

router = APIRouter()

@router.post("/register", status_code=201)
async def register_article(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    result = article_crud.add_article(request_article=dto)
    return {"data": result}

@router.put("/modify/{id}", status_code=201)
async def modify_article(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.update_article(request_article=dto)


@router.delete("/title/{title}/page/{page}", status_code=201)
async def delete(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.delete_article(request_article=dto)

@router.get("/page/{page}", status_code=201) #@router.get("/id/{user_id}/page/{page}", status_code=201)
async def get_all_articles(dto: ArticleDTO, db: Session = Depends(get_db)):
    ArticleCrud(db).find_all_articles(page=1)

@router.get("/id/{userid}/page/{page}", status_code=201)
async def get_article_by_userid(dto: ArticleDTO, db: Session = Depends(get_db)):
    article_crud = ArticleCrud(db)
    article_crud.find_article_by_userid(request_article=dto)
    '''
    #article = article_crud.find_article_by_userid(request_article=dto)
    result = article_crud.find_article_by_userid(request_article=dto)
    if article is not None:
        result = article_crud.get_article(request_article=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="열람 불가"))
    return result'''

@router.get("/seq/{seq}", status_code=201)
async def get_article_by_seq(dto: ArticleDTO, db: Session = Depends(get_db)):
    ArticleCrud(db).find_article_by_seq(request_article=dto)

@router.get("/title/{title}/page/{page}", status_code=201)
async def get_articles_by_title(title:str, dto: ArticleDTO, db: Session = Depends(get_db)):
    ArticleCrud(db).find_article_by_title(title=title,  request_article=dto)
