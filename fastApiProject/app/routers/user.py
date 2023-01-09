from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.repositories.user as dao
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_users(db : Session = Depends(get_db)):
    return {"data": dao.find_users(db = db)}
    #return {"data": find_users_legacy()}
