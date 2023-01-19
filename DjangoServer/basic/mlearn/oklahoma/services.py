import os

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5110 entries, 0 to 5109
Data columns (total 12 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   id                 5110 non-null   int64  
 1   gender             5110 non-null   object 
 2   age                5110 non-null   float64
 3   hypertension       5110 non-null   int64  
 4   heart_disease      5110 non-null   int64  
 5   ever_married       5110 non-null   object 
 6   work_type          5110 non-null   object 
 7   Residence_type     5110 non-null   object 
 8   avg_glucose_level  5110 non-null   float64
 9   bmi                4909 non-null   float64
 10  smoking_status     5110 non-null   object 
 11  stroke             5110 non-null   int64  
dtypes: float64(3), int64(4), object(5)
memory usage: 479.2+ KB
None
'''

class OklahomaService(object):

    def __init__(self):
        global data, save, oklahoma_origin
        data = os.path.join(os.getcwd(), "data" )
        save = os.path.join(os.getcwd(), "save" )
        oklahoma_origin = pd.read_csv(os.path.join(data, "comb32.csv"))

    '''
    1.스펙보기
    '''
    def spec(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(" --- 1.Shape ---")
        print(oklahoma_origin.shape)
        print(" --- 2.Features ---")
        print(oklahoma_origin.columns)
        print(" --- 3.Info ---")
        print(oklahoma_origin.info())
        print(" --- 4.Case Top1 ---")
        print(oklahoma_origin.head(1))
        print(" --- 5.Case Bottom1 ---")
        print(oklahoma_origin.tail(3))
        print(" --- 6.Describe ---")
        print(oklahoma_origin.describe())
        print(" --- 7.Describe All ---")
        print(oklahoma_origin.describe(include='all'))
    '''
    2.한글 메타데이터
    '''
    def rename_meta(self):
        global oklahoma
        oklahoma_meta = {
            'id': '아이디', 'gender': '성별', 'age': '나이',
            'hypertension': '고혈압',
            'heart_disease': '심장병',
            'ever_married': '기혼여부',
            'work_type': '직종',
            'Residence_type': '거주형태',
            'avg_glucose_level': '평균혈당',
            'bmi': '체질량지수',
            'smoking_status': '흡연여부',
            'stroke': '뇌졸중'
        }
        oklahoma = oklahoma_origin.rename(columns=oklahoma_meta)
        print(" --- 2.Features ---")
        print(oklahoma.columns)

    '''
    3.타깃변수(=종속변수 dependent, Y값) 설정
    입력변수(=설명변수, 확률변수, X값)
    타깃변수명: stroke (=뇌졸중)
    타깃변수값: 과거에 한 번이라도 뇌졸중이 발병했으면 1, 아니면 0
    인터벌 = ['나이','평균혈당','체질량지수']
    '''
    def interval(self):
        global adult_stoke
        interval = ['나이','평균혈당','체질량지수']
        print(f'--- 구간변수 타입 --- \n {oklahoma[interval].dtypes}')
        print(f'--- 결측값 있는 변수 --- \n {oklahoma[interval].isna().any()[lambda x: x]}')
        print(f'체질량 결측비율: {oklahoma["체질량지수"].isnull().mean():.2f}')
        # 체질량 결측비율: 0.03 는 무시한다
        pd.options.display.float_format = '{:.2f}'.format
        print(f'--- 구간변수 기초 통계량 --- \n{oklahoma[interval].describe()}')
        criterion = oklahoma['나이'] > 18
        adult_stoke = oklahoma[criterion]
        print(f'--- 성인객체스펙 --- \n{adult_stoke.shape}')
        # 평균혈당 232.64이하와 체질량지수 60.3이하를 이상치로 규정하고 제거함
        c1 = adult_stoke['평균혈당'] <= 232.64
        c2 = adult_stoke['체질량지수'] <= 60.3
        adult_stoke = adult_stoke[c1 & c2]
        print(f'--- 이상치 제거한 성인객체스펙 ---\n{adult_stoke.shape}')

    '''
    4.범주형 = ['성별', '심장병', '기혼여부', '직종', '거주형태','흡연여부', '고혈압']
    '''

    def ratio(self): # 해당 컬럼이 없음
        pass
    def norminal(self):
        category = ['성별', '심장병', '기혼여부', '직종', '거주형태', '흡연여부', '고혈압']
        print(f'범주형변수 데이터타입\n {adult_stoke[category].dtypes}')
        print(f'범주형변수 결측값\n {adult_stoke[category].isnull().sum()}')
        print(f'결측값 있는 변수\n {adult_stoke[category].isna().any()[lambda x: x]}')# 결측값이 없음
        adult_stoke['성별'] = OrdinalEncoder().fit_transform(adult_stoke['성별'].values.reshape(-1,1))
        adult_stoke['기혼여부'] = OrdinalEncoder().fit_transform(adult_stoke['기혼여부'].values.reshape(-1, 1))
        adult_stoke['직종'] = OrdinalEncoder().fit_transform(adult_stoke['직종'].values.reshape(-1, 1))
        adult_stoke['거주형태'] = OrdinalEncoder().fit_transform(adult_stoke['거주형태'].values.reshape(-1, 1))
        adult_stoke['흡연여부'] = OrdinalEncoder().fit_transform(adult_stoke['흡연여부'].values.reshape(-1, 1))
        oklahoma.to_csv(os.path.join(save,"oklahoma.csv"))

    def ordinal(self): # 해당 컬럼이 없음
        pass

    def target(self):
        pass

    def partition(self):
        pass

