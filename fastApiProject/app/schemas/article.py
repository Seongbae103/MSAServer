from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Article(BaseModel):
    art_seq : int
    title : str
    content : str
    create_at : datetime
    updated_at : datetime
    user_id: UUID

    class Config:
        orm_mode = True
