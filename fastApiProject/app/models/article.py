from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from app.database import Base
from app.models.mixins import TimestampMixin



class Article(Base, TimestampMixin):
    __tablename__ = "articles"
    art_seq = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20))
    content = Column(String(20))

    user_id = Column(UUIDType(binary=False), ForeignKey('users.user_id'), default=uuid4, nullable=True) # foreingkey는 원래 null허용 ForeignKey('테이블명.primarykey')
    user = relationship('User', back_populates='articles') #model.article의articles와 연결되는거 나타냄 user = relationship('User', bask_populates='연결되는 인스턴스')
    class Config:
        arbitrary_types_allowed = True