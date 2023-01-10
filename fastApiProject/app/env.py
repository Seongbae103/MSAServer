from sqlalchemy import create_engine

HOSTNAME = 'host.docker.internal'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'mydb'
CHARSET = 'utf8'
DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
engine = create_engine(DB_URL, echo=True)  # host로 안되면 localhost