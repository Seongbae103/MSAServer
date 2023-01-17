from abc import abstractmethod, ABCMeta
from typing import List

from sqlalchemy.orm import Session

from app.schemas.article import ArticleDTO


class ArticleBase(metaclass=ABCMeta):

    @abstractmethod
    def add_article(self, request_article: ArticleDTO) -> str: pass

    @abstractmethod
    def read_article(self, request_article: ArticleDTO): pass

    @abstractmethod
    def read_all_articles(self, request_article: ArticleDTO): pass

    @abstractmethod
    def update_article(self, request_article: ArticleDTO) -> str: pass

    @abstractmethod
    def delete_article(self, request_article: ArticleDTO) -> str: pass

    @abstractmethod
    def find_all_article(self, page:int) -> List[ArticleDTO]: pass

    @abstractmethod
    def find_article_by_userid(self, request_article: ArticleDTO) -> ArticleDTO: pass

    @abstractmethod
    def find_article_by_title(self, request_article: ArticleDTO) -> str: pass