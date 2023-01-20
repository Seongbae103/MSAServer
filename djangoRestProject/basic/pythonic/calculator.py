class Culcurator(object):
    def __init__(self, fi, op, se):
        self.fi = fi
        self.op = op
        self.se = se
        self.culc_result()

    def culc_result(self):
        fi = self.fi
        op = self.op
        se = self.se
        if op == "+":
            result = fi + se
        elif op == "-":
            result = fi - se
        elif op == "*":
            result = fi * se
        elif op == "/":
            result = fi / se
        elif op == "%":
            result = fi % se
        self.result = result

    def print_fi(self):
        print(f"{self.fi} {self.op} {self.se} = {self.result}")

    @staticmethod
    def print_menu():
        print("1. 계산")
        print("2. 계산 내역")
        print("3. 내역 삭제")
        print("4. 종료")
        return int(input("실행 : "))

    @staticmethod
    def new_culc():
        fi = int(input("첫번째 수 :"))
        op = input("연산자 : ")
        se = int(input("두번째 수 : "))
        return Culcurator(fi, op, se)

    @staticmethod
    def print_result(ls):
        print("###계산###")
        print("*******************")
        ([i.print_fi() for i in ls])
        print("*******************")


if __name__ == '__main__':
    ls = []
    while True:
        menu = Culcurator.print_menu()
        if menu == 1:
            print("계산")
            ls.append(Culcurator.new_culc())
            Culcurator.print_result(ls)
        elif menu == 2:
            print("계산 내역")
            Culcurator.print_result(ls)
        elif menu == 3:
            print("내역 삭제")
        elif menu == 4:
            print("종료")
            break
