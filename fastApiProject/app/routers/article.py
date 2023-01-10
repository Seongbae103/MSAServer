from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.repositories.article as dao
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_all_articles(db : Session = Depends(get_db)):
    return {"data": dao.find_all_articles(db = db)}
    #return {"data": find_users_legacy()}

@router.post("/{id}")
async def article(id:str, item: str, db: Session = Depends(get_db)):
    dao.article(id, item, db)
    return {"data": "success"}

@router.put("/{id}")
async def update(id:str, item: str, db: Session = Depends(get_db)):
    dao.update(id,item,db)
    return {"data": "success"}

@router.delete("/{id}")
async def delete(id:str, item: str, db: Session = Depends(get_db)):
    dao.delete(id,item,db)
    return {"data": "success"}

@router.get("/{page}")
async def get_articles(page: int, db: Session = Depends(get_db)):
    ls = dao.find_articles(page, db)
    return {"data": ls}

@router.get("/id/{id}")
async def get_article_by_id(id: str, db: Session = Depends(get_db)):
    dao.find_article_by_id(id, db)
    return {"data": "success"}

@router.get("/serch/{search}/{no}")
async def get_article_by_text(search:str, page: int, db: Session = Depends(get_db)):
    dao.find_articles_by_job(search, page, db)
    return {"data": "success"}
