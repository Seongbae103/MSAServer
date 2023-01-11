from app.database import conn
import pymysql
from sqlalchemy.orm import Session
from app.models.user import User

pymysql.install_as_MySQLdb()



def update(id, item, db):
    return None

def delete(id, item, db):
    return None

def login(id, db):
    return None

def join(item, db):
    return None

def find_users_by_job(search, page, db):
    return None
def find_users_legacy():
    cursor = conn.cursor()  # MySQL에 접속
    sql = "select * from users"  # 적용할 MySQL 명령어를 만들어서 sql 객체에 할당
    cursor.execute(sql)
    # conn.close()  # 위에 작업한 내용 서버에 저장
    return cursor.fetchall()

def find_users(page:int, db: Session):
    print(f" page number is {page}")
    return db.query(User).all()

def find_user_by_id(id, db):
    return None

if __name__ == '__main__':
    print(Session)

