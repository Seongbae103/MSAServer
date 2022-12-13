from dataclasses import dataclass

LS = ["종료", "oop", "fp", "p481", "nonlocal", "nonlacal 위치", "p.485-1", "p.485-2",
      ]

x = 10

@dataclass
class Oop:
    x = 20
    def menu_1(self):
        x = self.x
        print('oop출력 : '+str(x))


def menu_2():
    global x
    y = x + 20
    print('fp출력 : ' + str(y))

def menu_3():
    x = 11
    def B():
        x = 21
    B()
    print(x)

def menu_4():
    x = 11
    def A_2():
        nonlocal x
        x = 21
    A_2()
    print(x)

def menu_5():
    x = 12
    y = 120
    def B():
        x = 22
        def C():
            nonlocal x
            nonlocal y
            x = x + 30
            y = y + 300
            print(x)
            print(y)
        C()
    B()


def menu_6():
    print('global로 전역변수 사용')
    x = 20
    def B():
        x=30
        def C():
            global x
            x = x+30
            print(x)
        C()
    B()

c = 0
def menu_7():
    print('클로저 사용하기')
    a = 3
    b = 5
    def mul_add(x):
        nonlocal t
        t = t+ (a * x + b)
    mul_add()

    def mul_add_2(x):
        nonlocal t
        t =t+ (a * x - b)
    mul_add_2()
    return {'1':mul_add, '2':mul_add_2}




def menu_list():
    for i, j in enumerate(LS):
        print(f'{i}. {j}')
    return input('실행')


def menu_8():
    pass


if __name__ == '__main__':
    while True:
        menu = menu_list()
        if menu == "0": break
        elif menu == "1":
            Oop.menu_1()
        elif menu == "2":
            menu_2()
        elif menu == "3":
            menu_3()
        elif menu == "4":
            menu_4()
        elif menu == "5":
            menu_5()
        elif menu == "6":
            menu_6()
        elif menu == "7":
            c = menu_7()
            print('클로저1 : '+str(c['덧셈1'](2)))
            print('클로저1 : '+str(c['덧셈2'](2)))
        elif menu == "8":
            menu_8()
