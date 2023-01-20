import secrets
import string
from typing import Union, Any
from datetime import datetime, timedelta
import shortuuid
import jwt
from app.admin.utils import utc_seoul
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
# JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret
JWT_SECRET_KEY = "JWT_SECRET_KEY"
# JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_KEY"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def myuuid():
    alphabet = string.ascii_lowercase + string.digits
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(length=8)

def get_hashed_password(plain_password : str) -> str: #incode
    return password_context.hash(plain_password)

def verify_password(plain_password : str, hashed_password:str): #password에 대한 인증
    return password_context.verify(plain_password, hashed_password)

def generate_token(subject: Union[str, Any], expires_delta:int = None): #토큰 생성
    if expires_delta is not None:
        expires_delta = utc_seoul() + expires_delta
    else:
        expires_delta = utc_seoul() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = { "exp" : expires_delta, "sub" : str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    print(f"발급된 토큰 {encode_jwt}")
    return encode_jwt
def generate_token_by_secrets(): # 우리 방식에서는 안쓴다(장기적으로는 더 큰 문제가 생긴다)
    return secrets.token_urlsafe(32) #python 3.8 기준으로 32가 디폴트

def refresh_token(subject: Union[str, Any], expires_delta :int =None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_expiration_date():  #만료일
    return utc_seoul() + timedelta(days=3)