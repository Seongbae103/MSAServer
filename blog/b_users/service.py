import random
import string

import pandas as pd
from sqlalchemy import create_engine


class UserService(object):
    def __init__(self):
        pass

    def insert_users(self):
        df = self.create_dframe()

        engine = create_engine(
            "mysql+pymysql://root:root@localhost:3306/mydb",
            encoding='utf-8')
        df.to_sql(name='blog_users',
                  if_exists='append',
                  con=engine,
                  index=False)
    def create_dframe(self):

        df = [self.create_users() for i in range(100)]
        df = pd.DataFrame(df, columns=['blog_userid', 'email', 'nickname', 'password'])
        df['blog_userid'] = df['blog_userid'].astype(str)
        print(f"df 확인 {df}")
        return df

    def create_users(self):
        string_pool = string.ascii_lowercase
        blog_userid = random.randint(9999, 99999)
        email = str(blog_userid) + "@naver.com"
        nickname = ''.join(random.sample(string_pool, 5))
        password = 0
        return [blog_userid, email, nickname, password]

    def userid_checker(self): # 아이디 중복체크
        pass
        '''print('중복 확인')
        df = self.create_users()
        if df.duplicated(['blog_userid'], keep=False) == True:
            print('중복된 아이디입니다')
        else:
            return df'''



if __name__ == '__main__':
    UserService().insert_users()