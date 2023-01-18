from abc import ABC
from typing import List
from fastapi import HTTPException
from app.admin.security import verify_password
from app.bases.user import UserBase
from app.models.user import User
from app.schemas.user import UserDTO
import pymysql
from sqlalchemy.orm import Session
pymysql.install_as_MySQLdb()

class UserCrud(UserBase, ABC):

    def __init__(self, db: Session):
        self.db: Session = db

    def add_user(self, request_user: UserDTO) -> str:
        user = User(**request_user.dict())
        self.db.add(user)
        self.db.commit()
        return "success" #modules.apis.userAPI의 if(response.data === "success"){에 들어가는 내용

    def login_user(self, request_user: UserDTO) -> UserDTO:
        userid = self.find_userid_by_email(request_user)
        verified = verify_password(plain_password = request_user.password,
                                   hashed_password = target.password)
        if verified:
            return target
        else:
            return None

    def update_user(self, request_user: UserDTO) -> str:
        update_data = request_user.dict(exclude_unset=True)

        lastrowid = self.db.update(update_data)
        print(f" 수정완료 후 해당 ID : {lastrowid}")
        self.db.commit()
        return lastrowid

    def delete_user(self, request_user: UserDTO):
        target = self.find_user_by_id(request_user)
        self.db.delete(target)
        self.db.commit()
        return "success"

    def find_all_users(self, page: int) -> List[User]:
        return self.db.query(User).all()

    def find_user_by_id(self, request_user: UserDTO) -> UserDTO:
        user = User(**request_user.dict())
        return self.db.query(User).filter(User.user_id == user.user_id).first()

    def find_userid_by_email(self, request_user: UserDTO) -> str:
        user = User(**request_user.dict())
        db_user = self.db.query(User).filter(User.user_email == user.user_email).first()
        if db_user is not None:
            return db_user
        else:
            return ""