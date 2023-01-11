from app.database import conn
import pymysql
from sqlalchemy.orm import Session
from app.models.article import Article

pymysql.install_as_MySQLdb()

def find_article_legacy():
    cursor = conn.cursor()
    sql = "select * from articles"
    cursor.execute(sql)
    # conn.close()
    return cursor.fetchall()

def find_all_articles(db : Session):
    return db.query(Article).all()

def article(id, item, db):
    return None

def update(id, item, db):
    return None

def delete(id, item, db):
    return None

def find_articles(page, db):
    return None

def find_article_by_id(id, db):
    return None

def find_articles_by_job(search, page, db):
    return None