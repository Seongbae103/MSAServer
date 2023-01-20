from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from app.admin.security import myuuid
from app.database import Base
from app.models.mixins import TimestampMixin



class Article(Base, TimestampMixin):
    __tablename__ = "articles"
    art_seq = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    content = Column(String(30))
    user_id = Column(String(30), ForeignKey('users.user_id'), default=myuuid(), nullable=True) # foreingkey는 원래 null허용 ForeignKey('테이블명.primarykey')
    user = relationship('User', back_populates='articles')                                     #model.article의articles와 연결되는거 나타냄 user = relationship('User', bask_populates='연결되는 인스턴스')

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f'아이디: {self.user_id}, \n ' \
               f'글번호: {self.art_seq}, \n ' \
               f'제목: {self.title}, \n ' \
               f'내용: {self.content}, \n ' \
               f'작성일: {self.created} \n' \
               f'수정일: {self.modified}'