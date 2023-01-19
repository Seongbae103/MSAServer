from basic.dlearn.aitrader.models import AiTraderModel, DnnModel, DnnEnsemble, LstmModel, LstmEnsemble

menu = ["Exit",
        "Dnn Model",
        "Dnn Ensemble",
        "Lstm Model",
        "Lstm Ensemble"]
if __name__ == '__main__':
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(menu)]
        menu = input('메뉴선택: ')
        if menu == '0':
            print("종료")
            break
        else:
            try:
                if menu == "1": DnnModel().create()
                elif menu == "2": DnnEnsemble().create()
                elif menu == "3": LstmModel().create()
                elif menu == "4": LstmEnsemble().create()
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")
