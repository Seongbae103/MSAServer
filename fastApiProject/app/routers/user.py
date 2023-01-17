from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import app.cruds.user as dao
from app.admin.security import get_hashed_password, generate_token
from app.admin.utils import current_time
from app.database import get_db
from app.schemas.user import UserDTO

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(dto: UserDTO, db: Session = Depends(get_db)):
    print(f" 회원가입에 진입한 시간: {current_time()} ")
    print(f"SignUp Inform : {dto}")
    print(f"SignUp Inform : {dao.UserCrud(db)}")

    user_crud = dao.UserCrud(db)
    userid = user_crud.find_userid_by_email(request_user=dto)
    if userid =="":
        print(f"해시 전 비번 : {dto.password}")
        dto.password = get_hashed_password(dto.password)
        print(f"해시 후 비번 : {dto.password}")
        result = user_crud.add_user(request_user=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="이미 존재하는 이메일"))
    #result = dao.user_crud.add_user(dto)

    return {"data": result}

@router.post("/login", status_code=200)
async def login(dto: UserDTO, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    userid = user_crud.find_userid_by_email(request_user=dto)
    dto.user_id = userid
    print(f"로그인 전 확인 ID : {dto.user_id} / PW{dto.password}")
    if userid != "":
        login_user = user_crud.login(request_user=dto)
        if login_user is not None:
            print(f" 로그인 성공정보: {login_user}")
            new_token = generate_token(login_user.user_email)
            login_user.token = new_token
            result = login_user
        else:
            print(f" 로그인 실패")
            result = JSONResponse(status_code=400, content=dict(msg="틀린 비밀번호"))
    else:
        result = JSONResponse(status_code=400, content=dict(msg="없는 메일주소"))
    return result
@router.put("/modify/{id}")
async def update(id:str, item: UserDTO, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    user_crud.update_user(id, item)
    return {"data": "success"}

@router.delete("/delete/{id}")
async def delete(id: str, dto: UserDTO, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    user_crud.delete_user(request_article=dto)
    return {"data": "success"}

@router.get("/page/{page}")
async def get_users(page: int, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    ls = user_crud.find_user(page,db)
    return {"data": ls}

@router.get("/email/{id}")
async def get_user(id: str, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    user_crud.find_all_users(id, db)
    return {"data": "success"}

@router.get("/job/{search}/{page}")
async def get_users_by_job(search:str, page: int, db: Session = Depends(get_db)):
    user_crud = dao.UserCrud(db)
    user_crud.find_users_by_job(search, page,db)
    return {"data": "success"}
