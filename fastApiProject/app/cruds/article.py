from abc import ABC
from datetime import datetime
from typing import List, Set

import pytz
from fastapi import HTTPException

from app.bases.article import ArticleBase
import pymysql
from sqlalchemy.orm import Session
from app.models.article import Article

from app.schemas.article import ArticleDTO

pymysql.install_as_MySQLdb()

class ArticleCrud(ArticleBase, ABC):
    def __init__(self, db: Session):
        self.db: Session = db

    def add_article(self, request_article: ArticleDTO) -> str:
        print(f"### 1 ### {request_article}")
        article = Article(**request_article.dict())
        print(f"### 2 ### {article}")
        self.db.add(article)
        self.db.commit()
        print("### 3 ###")
        return "success"
    def read_article(self, request_article: ArticleDTO):
        article = Article(**request_article.dict())
        target = self.db.query(Article).filter(Article.user_id== article.user_id).first()
        if not target:
            raise HTTPException(status_code=404)
        return {"status":"success", "target" :target}

    def read_all_articles(self, request_article: ArticleDTO):
        article = Article(**request_article.dict())
        targets = self.db.query(Article).filter(Article.user_id == article.user_id).all()
        if not targets:
            raise HTTPException(status_code=404)
        return {"status": "success", "result":len(targets), "targets": targets}
    def update_article(self, request_article: ArticleDTO):
        article = Article(**request_article.dict())
        target = self.find_article_by_title(request_article)
        target.content = article.content
        target.modified = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        self.db.add(target)#업데이트는 뭐로?
        self.db.commit()
        return "success"

    def delete_article(self, request_article: ArticleDTO) -> str:
        target = self.find_article_by_title(request_article)
        self.db.delete(target)
        self.db.commit()
        return "success"


    def find_all_article(self, page: int) -> List[ArticleDTO]:
        pass

    def find_article_by_title(self, request_article: ArticleDTO) -> str:
        article = Article(**request_article.dict())
        return self.db.query(Article).filter(Article.title == article.title).first()

    def find_article_by_userid(self, request_article: ArticleDTO) -> str:
        article = Article(**request_article.dict())
        return self.db.query(Article).filter(Article.user_id == article.user_id).first()

