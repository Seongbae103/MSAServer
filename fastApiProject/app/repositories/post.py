from app.database import conn
import pymysql
from sqlalchemy.orm import Session
from app.models.post import Post

pymysql.install_as_MySQLdb()

def find_post_legacy():
    cursor = conn.cursor()
    sql = "select * from users"
    cursor.execute(sql)
    # conn.close()
    return cursor.fetchall()

def find_post(db : Session):
    return db.query(Post).all()
