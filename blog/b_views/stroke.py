import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from imblearn.under_sampling import RandomUnderSampler

STROKE_MENUS = ["종료", #0
                "데이터구하기",#1
                "한글화"#2
                "타깃변수설정",#3
                "데이터처리",#4
                "시각화",#5
                "모델링",#6
                "학습",#7
                "예측"]#8
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
stroke_meta = {
    'id':'아이디',
    'gender':'성별',
    'age':'나이',
    'hypertension':'고혈압',
    'heart_disease':'심장병',
    'ever_married':'기혼여부',
    'work_type':'직종',
    'Residence_type':'거주형태',
    'avg_glucose_level':'평균 혈당',
    'bmi':'체질량지수',
    'smoking_status':'흡연 여부',
    'stroke':'뇌졸중'
}
stroke_menu = {
    "1" : lambda t: t.menu_1(),
    "2" : lambda t: t.menu_2(),
    "3" : lambda t: t.interval_variables(),
    "4" : lambda t: t.menu_4(),
    "5" : lambda t: t.sampling(),
    "99" : lambda t: t.visual()
}
class StrokeService:
    def __init__(self):
        self.stroke = pd.read_csv('../static/data/dam_crime/healthcare-dataset-stroke-data.csv')
        self.my_stroke = None
    '''
    1.스펙보기
    '''
    def menu_1(self):
        print(" --- 1.Shape ---")
        print(self.stroke.shape)
        print(" --- 2.Features ---")
        print(self.stroke.columns)
        print(" --- 3.Info ---")
        print(self.stroke.info())
        print(" --- 4.Case Top1 ---")
        print(self.stroke.head(1))
        print(" --- 5.Case Bottom1 ---")
        print(self.stroke.tail(3))
        print(" --- 6.Describe ---")
        print(self.stroke.describe())
        print(" --- 7.Describe All ---")
        print(self.stroke.describe(include='all'))
    '''
    2.한글 메타데이터
    '''
    def menu_2(self):
        self.my_stroke = self.stroke.rename(columns=stroke_meta)
        return self.my_stroke

    '''
    3. 타깃변수(=종속변수 dependent, y값) 설정
    입력변수(= 설명변수, 확률변수, X값)
    타깃변수명 :stroke (=뇌졸중)
    타깃 변수값 : 과거에 한 번이라도 뇌졸중이 발병했으면 1, 아니면 0
    '''
    def interval_variables(self):
        print(self.my_stroke['아이디'].dtypes)
        print(self.my_stroke['아이디'].isnull().sum())
        print(len(pd.unique(self.my_stroke['아이디'])))
        print(self.my_stroke['뇌졸중'].dtype)
        print(self.my_stroke['뇌졸중'].isnull().sum())
        print(self.my_stroke['뇌졸중'].value_counts(dropna=False, normalize=True))

    def menu_4(self):
        df= self.my_stroke
        cols = ['나이', '평균 혈당', '체질량지수']
        print(df[cols].dtypes)
        pd.options.display.float_format = '{:.2f}'.format
        print(df[cols].describe())
        c = df['나이'] > 18
        print(df[c].head(3))
        len(df[c])
        print(len(df[c])/ len(df))
        df1 = df[c]
        df1 = df1.rename(columns={'Residence_type': 'residence_type'})
        print(df1.shape)
        cols1 = ['성별', '고혈압', '심장병', '기혼여부', '직종', '거주형태', '흡연 여부']
        print(df1[cols1].isnull().sum())
        print(df1.isna().any()[lambda x: x])
        print(df['체질량지수'].isnull().mean())
        print(df1[cols].describe())
        print(df1[cols].skew())
        print(df1[cols].kurtosis())
        print(df1['직종'].value_counts(dropna=False))
        print(pd.crosstab(df1['직종'], columns= 'count'))
        print(pd.crosstab(df1['직종'], columns= 'ratio', normalize=True))
        print(pd.crosstab(df1['직종'], df1['뇌졸중']))
        print(pd.crosstab(df1['직종'], df1['뇌졸중'], normalize = True))
        '''이상값 제거(p.83)'''
        fig, axes = plt.subplots(1, 3, figsize=(15,4))
        sns.histplot(ax=axes[0], data=df, x="나이", kde=True, bins=20)
        sns.histplot(ax=axes[1], data=df, x="평균 혈당", kde=True, bins=20)
        sns.histplot(ax=axes[2], data=df, x="체질량지수", kde=True, bins=20)
        plt.show()
        '''구간 변수상자(p86)'''
        sns.boxplot(ax=axes[0], x="나이", data=df1)
        sns.boxplot(ax=axes[1], x="평균 혈당", data=df1)
        sns.boxplot(ax=axes[2], x="체질량지수", data=df1)
        '''구간변수의 IQR계산 (p.86)'''
        Q1 = df1[['나이', '평균 혈당', '체질량지수']].quantile(0.25)
        Q3 = df1[['나이', '평균 혈당', '체질량지수']].quantile(0.75)
        IQR = Q3 - Q1
        print(IQR)
        '''IQR 상한, 하한'''
        Lower = Q1-3.0*IQR
        Upper = Q3+3.0*IQR
        print(Lower)
        print(Upper)
        c1 = df1['평균 혈당'] <= 232.64
        c2 = df1['체질량지수'] <= 60.3
        df2 = df1[c1 & c2]
        print(df2.shape)
        '''상관계수 검토'''
        print('이상치 제거한 성인개체')
        round(df2[cols].corr(),2)
        corr = df2[cols].corr()
        annot_kws ={"ha" : 'center', "va": 'top'}
        sns.heatmap(data=corr, annot= True, annot_kws=annot_kws, cmap="YlGnBu")


    '''
    4.범주형 = ['성별', '심장병', '기혼여부', '직종', '거주형태','흡연여부', '고혈압']
    '''
    def nominal_variables(self):
        t = self.df2
        category = ['성별', '심장병', '기혼여부', '직종', '거주형태', '흡연여부', '고혈압']
        print(f'범주형변수 데이터타입\n {t[category].dtypes}')
        print(f'범주형변수 결측값\n {t[category].isnull().sum()}')
        print(f'결측값 있는 변수\n {t[category].isna().any()[lambda x: x]}')  # 결측값이 없음
        t['성별'] = OrdinalEncoder().fit_transform(t['성별'].values.reshape(-1, 1))
        t['기혼여부'] = OrdinalEncoder().fit_transform(t['기혼여부'].values.reshape(-1, 1))
        t['직종'] = OrdinalEncoder().fit_transform(t['직종'].values.reshape(-1, 1))
        t['거주형태'] = OrdinalEncoder().fit_transform(t['거주형태'].values.reshape(-1, 1))
        t['흡연여부'] = OrdinalEncoder().fit_transform(t['흡연여부'].values.reshape(-1, 1))

        self.stroke = t
        self.spec()
        print(" ### 프리프로세스 종료 ### ")
        self.stroke.to_csv("./save/stroke.csv")

    def ordinal_variables(self): #해당 column이 없음
        pass

    def sampling(self):
        df = pd.read_csv('./save/stroke.csv')
        data = df.drop(['뇌졸중'], axis=1)
        undersample = RandomUnderSampler(sampling_strategy=0.333, random_state=2)
        target = df['뇌졸중']
        data_under, target_under = undersample.fit_resample(data, target)
        print(target_under.value_counts(dropna=True))
        x_train, x_test, y_train, y_test = train_test_split(data_under, target_under, test_size=0.5, random_state=42, stratify=target_under)
        print("x_train shape : ", x_train.shape)
        print("x_test shape : ", x_test.shape)
        print("y_train shape : ", y_train.shape)
        print("y_test shape : ", y_test.shape)
        print(y_train.value_counts(normalize=True))
        print(y_train.value_counts())



    '''
    5. 시각화
    '''
    def visual(self):
        df = self.my_stroke
        '''나이에 대한 그래프'''
        print(sns.histplot(data=df, x='나이', hue="뇌졸중", bins=20))
        '''나이의 타깃변수'''
        sns.set_style('whitegrid')
        print(sns.boxplot(x='뇌졸중', y='나이', data=df))
        '''각 상자의 평균'''
        group = df['나이'].groupby(df['뇌졸중'])
        print(group.mean())
        plt.show()
        df.to_csv("./save/stroke.csv", index=False)
def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = StrokeService()
    while True:
        menu = my_menu(STROKE_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            try:
                stroke_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")