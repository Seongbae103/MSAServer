from sqlalchemy import create_engine
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.env import HOSTNAME, PORT, USERNAME, PASSWORD, DATABASE, CHARSET, DB_URL


Base = declarative_base()
engine = create_engine(DB_URL, echo=True)  # host로 안되면 localhost
pymysql.install_as_MySQLdb()
conn = pymysql.connect(host=HOSTNAME, port=PORT, user=USERNAME, password=PASSWORD, db=DATABASE, charset=CHARSET)
SessionLocal = scoped_session(
    sessionmaker(autocommit= False, autoflush= False, bind=engine)
)
Base.query = SessionLocal.query_property()

def get_db():
    try:
        db = SessionLocal()
        yield db #조건이 맞으면 실행
    finally:
        db.close()