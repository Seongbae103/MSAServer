'''
두자리 정수 랜덤숫자 10개를 뽑아서
사용자가 검색하는 숫자의 배수만 출력하는
프로그램을 개발하시오.
예) [12, 23, 48,...,]
사용자의 input 값이 12인 경우
출력값이 12, 48만 되도록 한다.
'''
from multiplex.randomlist import RandomList

class SearchNumber(object):
    def __init__(self, num):
        self.num = num

    def print_menu(self):
        rl = RandomList().get_random(10, 100, 10)
        print(rl)
        for i in rl:
            if i % self.num == 0:
                print(f"{i}")

if __name__ == '__main__':
    num = int(input("input : "))
    searchnumber = SearchNumber(num)
    searchnumber.print_menu()