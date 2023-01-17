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