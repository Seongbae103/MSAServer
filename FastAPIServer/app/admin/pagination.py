from starlette.responses import JSONResponse
from app.database import get_db
from app.cruds.user import UserCrud
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/page")
def pagination(db: Session = Depends(get_db)):
    # 필드값(이미 존재하는 값)
    row_cnt = UserCrud(db).count_all_users()
    page_size = 5
    t = row_cnt // page_size
    t2 = row_cnt % page_size
    page_cnt = t if (t2 == 0) else t + 1

    block_size = 0
    t = page_cnt // block_size
    t2 = page_cnt % block_size
    block_cnt = t if (t2 == 0) else t + 1

    #index
    page_now = 0  # 사용자가 선택한 페이지
    row_start = page_size * (page_now-1)
    row_end = row_start+page_size-1 if page_now != page_cnt else row_cnt-1

    block_now = page_now // block_size
    page_start = block_size *block_size

    page_end = page_start+block_size-1 if block_now != block_cnt else page_cnt
    block_start = 0
    block_end = 0

    block_size = 0 # 고객이 원하는 글이 있는 블럭

    '''# 필드값(이미 존재하는 값)
    row_cnt = 0
    page_cnt = 0
    block_cnt = 0

    # index
    row_start = 0
    row_end = 0
    page_start = 0
    page_end = 0
    block_start = 0
    block_end = 0
    page_size = 0
    block_size = 0
    # 상태값(외부에서 주입되는 값), payload
    page_now = 0  # 고객이 원하는 글이 있는 페이지
    block_size = 0  # 고객이 원하는 글이 있는 블럭'''


    count = UserCrud(db).count_all_users()
    print(f" count is {row_cnt}")
    return JSONResponse(status_code=200,
                        content=dict(
                            msg=row_cnt))

