from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.admin.security import get_hashed_password, generate_token
from app.admin.utils import current_time
from app.cruds.user import UserCrud
from app.database import get_db
from app.schemas.user import UserDTO

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(dto: UserDTO, db: Session = Depends(get_db)):
    print(f" 회원가입에 진입한 시간: {current_time()} ")
    user_crud = UserCrud(db) #이 함수가 끝나면 무상태로 돌아가야되기 때문에 db를 전역으로 남기지 않는다.
    userid = user_crud.find_userid_by_email(request_user=dto)
    if userid =="":
        dto.password = get_hashed_password(dto.password)
        result = user_crud.add_user(request_user=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="이미 존재하는 이메일"))
    #result = dao.user_crud.add_user(dto)
    return {"data": result}

@router.post("/login", status_code=200)
async def login(dto: UserDTO, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)
    token_or_fail_message = user_crud.find_userid_by_email(request_user=dto)
    return JSONResponse(status_code=200, content=dict(msg=token_or_fail_message))


@router.get("/page/{page}")
async def get_user(dto: UserDTO, db: Session = Depends(get_db)):
    return UserCrud(db).find_user_by_id(request_user=dto)

@router.put("/modify/{id}")
async def update(id:str, item: UserDTO, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)
    user_crud.update_user(id, item, db)
    return {"data": "success"}

@router.delete("/delete/{id}")
async def delete(dto: UserDTO, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)
    user = user_crud.find_user_by_id(request_user=dto)
    if user is not None:
        result = user_crud.delete_user(request_user=dto)
    else:
        result = JSONResponse(status_code=400, content=dict(msg="작성 불가"))
    return {"data": result}

