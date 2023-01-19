from basic.dlearn.fashion.services import FashionService

if __name__ == '__main__':
    menu = ["Exit", "Find Fashion by Index"]  # 1
    menu_lambda = {
        "1": lambda x: x.find_fashion_by_index(1),
    }
    service = FashionService()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(menu)]
        menu = input('메뉴선택: ')
        if menu == '0':
            print("종료")
            break
        else:
            try:
                menu_lambda[menu](service)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")