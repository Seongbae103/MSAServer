from abc import ABC
from typing import List, Set
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
        article = Article(**request_article.dict())
        self.db.add(article)
        self.db.commit()
        return "success"

    def get_article(self, request_article: ArticleDTO):
        article = Article(**request_article.dict())
        target = self.find_article_by_seq(article)
        return {"status":"success", "target" :target}

    def get_all_articles(self, request_article: ArticleDTO):
        article = Article(**request_article.dict())
        targets = self.find_article_by_userid(article)
        return {"status": "success", "result":len(targets), "targets": targets}

    def update_article(self, request_article: ArticleDTO):
        update_data = self.find_article_by_seq(request_article)
        self.db.update(update_data)
        self.db.commit()
        return "success"

    def delete_article(self, request_article: ArticleDTO) -> str:
        target = self.find_article_by_seq(request_article)
        self.db.delete(target)
        self.db.commit()
        return "success"

    def find_all_articles(self, page: int) -> List[ArticleDTO]:
        return self.db.query(Article).all()

    def find_article_by_userid(self, request_article: ArticleDTO) -> str:
        article = Article(**request_article.dict())
        return self.db.query(Article).filter(Article.user_id == article.user_id).first()

    def find_article_by_title(self, request_article: ArticleDTO) -> str:
        article = Article(**request_article.dict())
        return self.db.query(Article).filter(Article.title == article.title).first()

    def find_article_by_seq(self, request_article: ArticleDTO) -> ArticleDTO:
        article = Article(**request_article.dict())
        return self.db.query(Article).filter(Article.art_seq == article.art_seq).first()