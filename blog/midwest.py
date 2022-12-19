import numpy as np
import pandas as pd

Mw_MENUS = ["종료",
         "메타데이터 출력",
         "poptotal/popasian 변수를 total/asian로 이름변경",
         "전체 인구 대비 아시아 인구 백분율 변수 추가",
         "아시아 인구 백분율 전체 평균을 large/small 로 분류",
         "large/small 빈도표와 빈도막대그래프 작성"]
mw_menu = {
    "1" : lambda t: t.menu_1(),
    "2" : lambda t: t.menu_2(),
    "3" : lambda t: t.menu_3(),
    "4" : lambda t: t.menu_4(),
    "5" : lambda t: t.menu_5()
}

class Midwest(object):
    def __init__(self):
        self.md = pd.read_csv('data/dam_pd_samples/midwest.csv')
        self.md2 = None

    def menu_1(self):
        print('###메타데이터 출력###')
        print(self.md.head())
    def menu_2(self):
        md = self.md
        print('###poptotal/popasian 변수를 total/asian로 이름변경###')
        self.md2 = md.rename(columns={'poptotal' : 'total','popasian' : 'asian'})
        print(self.md2)
    def menu_3(self):
        print('###전체 인구 대비 아시아 인구 백분율 변수 추가###')
        self.menu_2()
        t = self.md2
        t = t.assign(per = (t['asian']/t['total'])*100)
        self.md2 = t
        print(self.md2)
    def menu_4(self):
        print('###아시아 인구 백분율 전체 평균을 기준으로 large/small 로 분류###')
        self.menu_3()
        t = self.md2
        t['group'] = np.where(t['pd_samples'] >= t['pd_samples'].mean(), 'large', 'small' )
        return t['group']
    def menu_5(self):
        print('###large/small 빈도표와 빈도막대그래프 작성###')
        self.menu_4()
        md2 = self.md2
        result = md2['group'].value_counts()
        print(result)
        print(result.plot.bar(rot = 0))

def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = Midwest()
    while True:
        menu = my_menu(Mw_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            try:
                mw_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")