import string

import numpy as np
import pandas as pd
MENU = ["종료", "과일2D", "숫자2D"]
def fruits():
    ls1 = ['제품', '가격', '판매']
    ls2 = ['사과', '딸기', '수박']
    ls3 = [1800, 1500, 3000]
    ls4 = [24, 38, 13]
    column = [ls2, ls3, ls4]
    df = pd.DataFrame({j : column[i] for i, j in enumerate(ls1)})
    print(df)
    print('가격 평균 : '+ str(df['가격'].mean()))
    print('판매량 평균 : '+ str(df['판매'].mean()))

def new_number_2d():
    df = pd.DataFrame(np.array([list(range(1,11)),
                                list(range(11,21)),
                                list(list(range(21,31)))]),
                      columns=list(string.ascii_lowercase)[:10])
    print(df)

def type_check():
    a = pd.DataFrame()
    print(type(a))
def menus():
    for i, j in enumerate(MENU):
        print(f' {i}. {j}')
    return input('실행 : ')

if __name__ == '__main__':
    while True:
        menu = menus()
        if menu == "0":
            break
        elif menu == "1":
            fruits()
        elif menu == "2":
            new_number_2d()
        elif menu == "100":
            type_check()
        else: print('잘못 입력')
