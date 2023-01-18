from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class ArticleDTO(BaseModel):
    art_seq : Optional[int]
    title : Optional[str]
    content : Optional[str]
    created : Optional[str]
    modified : Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True

class ArticleUpdate(BaseModel):
    art_seq: Optional[str]
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[str]
    modified: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True