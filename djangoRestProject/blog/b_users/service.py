import random
import string
import pandas as pd
from sqlalchemy import create_engine

from basic.algorithms.lambdas import lambda_number, lambda_string, lambda_k_name, random_number


class UserService(object):
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:root@localhost:3306/mydb",
            encoding='utf-8')

    def insert_users(self):
        '''
        기본 순서
        dc = self.create_user() #개인
        ls = self.create_users(dc) # 다수
        df = self.change_to_df_users(ls) # 데이터프레임
        df.to_sql(name='blog_users',
                  if_exists='append',
                  con=self.engine,
                  index=False)
        '''
        df = self.create_dframe()
        df.to_sql(name='blog_users',
                  if_exists='append',
                  con=self.engine,
                  index=False)

    def create_user(self) -> []:
        blog_userid = lambda_number(4)
        email = str(blog_userid) + "@naver.com"
        nickname = lambda_string(5)
        password = 0
        username = lambda_k_name(2)
        birth = str(random_number(1, 13) + '.' + str(random_number(1, 30)))
        return [blog_userid, email, nickname, password, username, birth]

    def create_dframe(self) -> {}:
        df = [self.create_user() for _ in range(100)]
        df = pd.DataFrame(df, columns=['blog_userid', 'email', 'nickname', 'password', 'username', 'birth'])
        df['blog_userid'] = df['blog_userid'].astype(str)
        print(f"df 확인 {df}")
        return df
    def change_to_df_users(self):
        pass

    def get_users(self):
        pass

    def userid_checker(self): # 아이디 중복체크
        pass
        '''print('중복 확인')
        df = self.create_user()
        if df.duplicated(['blog_userid'], keep=False) == True:
            print('중복된 아이디입니다')
        else:
            return df
        '''


if __name__ == '__main__':
    UserService().create_dframe()