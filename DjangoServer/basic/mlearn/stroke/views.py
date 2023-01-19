
stroke_lambda = {
    "1" : lambda x: x.hook(),
}
if __name__ == '__main__':
    stroke = Stroke()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(["Exit","Learning"])]
        menu = input('메뉴선택: ')
        if menu == '0':
            print("종료")
            break
        else:
            try:
                stroke_lambda[menu](stroke)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")