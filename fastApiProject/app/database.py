import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.env import HOSTNAME, PORT, USERNAME, PASSWORD, DATABASE, CHARSET, engine

Base = declarative_base()
pymysql.install_as_MySQLdb()
conn = pymysql.connect(host=HOSTNAME, port=PORT, user=USERNAME, password=PASSWORD, db=DATABASE, charset=CHARSET)
SessionLocal = scoped_session(
    sessionmaker(autocommit= False, autoflush= False, bind=engine)
)
Base.query = SessionLocal.query_property()

async def get_db():
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
    finally:
        db.close()

async def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise e