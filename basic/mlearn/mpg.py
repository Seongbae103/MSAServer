import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

MENUS = ["종료",
         "mpg 앞부분 확인",
         "mpg 뒷부분 확인",
         "행,열 출력",
         "데이터 속성 확인",
         "요약 통계량 출력",
         "문자 변수 요약 통계량 함께 출력",
         "menufacturer를 company로 변경",
        "test 변수 생성",
        # cty 와 hwy 변수를 머지(merge)하여 total
         # 변수 생성하고 20이상이면 pass 미만이면 fail 저장
         "test 빈도표 만들기", "test 빈도 막대 그래프 그리기",
         # mpg 144페이지 문제
         "displ(배기량)이 4이하와 5이상 자동차의 hwy(고속도로 연비) 비교",
         "아우디와 토요타 중 도시연비(cty) 평균이 높은 회사 검색",
         "쉐보레, 포드, 혼다 데이터 출력과 hwy 전체 평균",
         # mpg 150페이지 문제
         # 메타데이터가 category, cty 데이터는 해당 raw 데이터인 객체생성
         # 후 다음 문제 풀이
         "suv / 컴팩 자동차 중 어떤 자동차의 도시연비 평균이 더 높은가?",
         # mpg 153페이지 문제
         "아우디차에서 고속도로 연비 1~5위 출력하시오",
         # mpg 158페이지 문제
         "평균연비가 가장 높은 자동차 1~3위 출력하시오",
         ]
ls = []
'''
Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   Unnamed: 0    234 non-null    int64  
 1   manufacturer : 회사  234 non-null    object 
 2   model : 모델        234 non-null    object 
 3   displ : 배기량         234 non-null    float64
 4   year : 연식         234 non-null    int64  
 5   cyl : 실린더          234 non-null    int64  
 6   trans : 차축        234 non-null    object 
 7   drv : 오토          234 non-null    object 
 8   cty : 시내연비          234 non-null    int64  
 9   hwy : 시외연비          234 non-null    int64  
 10  fl : 연료            234 non-null    object 
 11  class : 차종         234 non-null    object 
dtypes: float64(1), int64(5), object(6)
'''
my_meta = {
    "manufacturer": "회사",
    "model": "모델",
    "displ": "배기량",
    "year": "연식",
    "cyl": "실린더",
    "trans": "차축",
    "drv": "오토",
    "cty": "시내연비",
    "hwy": "시외연비",
    "fl": "연료",
    "class": "차종"
}

mpg = pd.read_csv('../../blog/data/dam_pd_samples/mpg.csv')

class MpgService(object):
    def __init__(self):
        self.mpg = pd.read_csv('../../blog/data/dam_pd_samples/mpg.csv')
        self.my_mpg = None
        self.count_test = None
    def menu_1(self):
        print(self.mpg.head())
    def menu_2(self):
        print(self.mpg.tail())
    def menu_3(self):
        print(self.mpg.shape)
    def menu_4(self):
        print(self.mpg.info())
    def menu_5(self):
        print(self.mpg.describe())
    def menu_6(self):
        print(self.mpg.describe(include='all'))
    def menu_7(self):
        self.my_mpg = self.mpg.rename(columns=my_meta)
    def menu_8(self):
        self.menu_7()
        t = self.my_mpg
        print('###test 변수 생성###')
        t['총연비'] = (t['시내연비'] + t['시외연비']) / 2
        t['연비테스트'] = np.where(t['총연비'] >= 20, 'pass', 'fail')
        self.my_mpg = t
        print(self.my_mpg)
    def menu_9(self):
        self.menu_8()
        t = self.my_mpg
        self.count_test = t['연비테스트'].value_counts()
        print(self.count_test)
        self.my_mpg = t
    def menu_10(self):
        self.menu_9()
        self.count_test.plot.bar(rot=0)
        plt.savefig('./save/test.png')
    def menu_11(self):
        mpg_4 = mpg.query('배기량 <= 4')
        mpg_5 = mpg.query('배기량 >= 5')
        avg_4 = sum(mpg.query('배기량 <= 4')['시외연비'])/len(mpg_4)
        avg_5 = sum(mpg.query('배기량 >= 5')['시외연비'])/len(mpg_5)
        if avg_4 > avg_5:
            print('***배기량 4 이하의 연비가 더 좋다***')
        elif avg_4 < avg_5:
            print('***배기량 5 이상의 연비가 더 좋다***')
    def menu_12(self):
        self.menu_7()
        print('###아우디와 토요타 중 도시연비(cty) 평균이 높은 회사 검색###')
        t = self.my_mpg
        audi = t.query("회사 == 'audi'")['시내연비'].mean()
        toyota = t.query("회사 == 'toyota'")['시내연비'].mean()
        if audi > toyota:
            print('***audi의 도시 연비 평균이 더 좋다***')
        elif audi < toyota:
            print('***toyota의 도시 연비 평균이 더 좋다***')
    def menu_13(self):
        self.menu_7()
        com = self.my_mpg.query("회사 == 'chevrolet' | 회사 == 'ford' | 회사 == 'honda'")['시외연비'].mean()
        print(com)
    def menu_14(self):
        '''self.menu_7()
        print(self.my_mpg[['차종', '시내연비']])''' # p150 문제1
        self.menu_7()
        compact = self.my_mpg.query("차종 == 'compact'")['시내연비'].mean()
        suv = self.my_mpg.query("차종 == 'suv'")['시내연비'].mean()
        if compact > suv:
            print('compact의 연비가 더 좋다')
        elif compact < suv:
            print('suv의 연비가 더 좋다')
    def menu_15(self):
        self.menu_7()
        audi = self.my_mpg.query("차종 == 'audi'")
        print(audi.sort_values(['시외연비'], ascending=[False]).head(5))
    def menu_16(self):
        self.menu_7()
        t = self.my_mpg
        rank = t.assign(total = t['시내연비'] + t['시외연비'], mean = lambda x: x[t['시내연비'] + t['시외연비']]/3).head(3)
        print(rank)


def my_menu(ls):
    for i, j in enumerate(ls):
        print(f'{i}. {j}')
    return (input('메뉴 : '))

if __name__ == '__main__':
    tt = MpgService()
    while True:
        menu = my_menu(MENUS)
        if menu == '0': break
        elif menu == '1':
            print(f'###mpg 앞부분 확인###')
            tt.menu_1()
        elif menu == '2':
            print('###mpg 뒷부분 확인###')
            tt.menu_2()
        elif menu == '3':
            print('###행,열 출력###')
            tt.menu_3()
        elif menu == '4':
            print('###데이터 속성 확인###')
            tt.menu_4()
        elif menu == '5':
            print('###요약 통계량 출력###')
            tt.menu_5()
        elif menu == '6':
            print('###문자 변수 요약 통계량 함께 출력###')
            tt.menu_6()
        elif menu == '7':
            tt.menu_7()
        elif menu == '8':
            tt.menu_8()
        elif menu == '9':
            tt.menu_9()
        elif menu == '10':
            tt.menu_10()
        elif menu == '11':
            tt.menu_11()
        elif menu == '12':
            tt.menu_12()
        elif menu == '13':
            tt.menu_13()
        elif menu == '14':
            tt.menu_14()
        elif menu == '15':
            tt.menu_15()
        elif menu == '16':
            tt.menu_16()
        else: print('없는 메뉴')