from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.repositories.post as dao
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_posts(db : Session = Depends(get_db)):
    return {"data": dao.find_post(db = db)}
    #return {"data": find_users_legacy()}
