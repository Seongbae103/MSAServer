from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.repositories.user as dao
from app.database import get_db
from app.schemas.user import User

router = APIRouter()

@router.post("/")
async def join(item: User, db: Session = Depends(get_db)):
    return {"data": "success"}

@router.post("/{id}")
async def login(id:str,item: User, db: Session = Depends(get_db)):
    dao.login(id, item, db)
    return {"data": "success"}

@router.put("/{id}")
async def update(id:str, item: User, db: Session = Depends(get_db)):
    dao.update(id, item, db)
    return {"data": "success"}

@router.delete("/{id}")
async def delete(id:str, item: User, db: Session = Depends(get_db)):
    dao.delete(id, item, db)
    return {"data": "success"}

@router.get("/{page}")
async def get_users(page: int, db: Session = Depends(get_db)):
    print(f"##############get_users #########")
    return {"data": dao.find_users(page, db=db)}


@router.get("/email/{id}")
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    dao.find_user_by_id(id, db)
    return {"data": "success"}

@router.get("/job/{search}/{page}")
async def get_users_by_job(search:str, page: int, db: Session = Depends(get_db)):
    dao.find_users_by_job(search, page, db)
    return {"data": "success"}
