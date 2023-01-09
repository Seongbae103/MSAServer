from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    title = Column(String(20))
    content = Column(String(20))
    create_at = Column(String(20))
    updated_at = Column(String(20))

    class Config:
        arbitrary_types_allowed = True
