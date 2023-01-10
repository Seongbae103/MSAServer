from pydantic import BaseModel


class User(BaseModel):
    user_email : str
    password : str
    user_name : str
    phone : str
    birth : str
    address : str
    job : str
    user_interests : str
    token : str
    create_at = str
    updated_at = str #여기의 구조는 인간이 해야하지만 데이터 클래스는 pydantic이 처리 가능

    class Config:
        orm_mode = True