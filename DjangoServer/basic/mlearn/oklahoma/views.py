from basic.mlearn.oklahoma.services import OklahomaService


oklahoma_menu = ["종료", #0
                "데이터구조파악",#1
                "변수한글화",#2
                "연속형변수편집",#3 18세이상만 사용함
                "범주형변수편집",#4
                "샘플링",#5
                "모델링",#6
                "학습",#7
                "예측"]#8
oklahoma_lambda = {
    "1" : lambda x: x.spec(),
    "2" : lambda x: x.rename_meta(),
    "3" : lambda x: x.interval_variables(),
    "4" : lambda x: x.categorical_variables(),
    "5" : lambda x: x.sampling(),
    "6" : lambda x: print(" ** No Function ** "),
    "7" : lambda x: print(" ** No Function ** "),
    "8" : lambda x: print(" ** No Function ** "),

}
if __name__ == '__main__':
    service = OklahomaService()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(oklahoma_menu)]
        menu = input('메뉴선택: ')
        if menu == '0':
            print("종료")
            break
        else:
            try:
                oklahoma_lambda[menu](service)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")