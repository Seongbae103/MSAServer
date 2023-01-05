'''
아이디, 비밀번호, 이름을 받아서
회원가입, 목록, 탈퇴하는 프로그램을 개발하시오.
'''


MENUS = ['회원가입', '회원 목록', '회원 삭제', '종료']
member_menu = {
        "1": lambda t: t.re_user(),
        "2": lambda t: t.print_list(),
        "3": lambda t: t.delete(ls, id),
    }

class Member(object):
    def __init__(self, name, num, id):
        self.name = name
        self.num = num
        self.id = id

    def new_user(self):
        return (input("아이디 : "),
                  input("비밀번호 : "),
                   input("이름 : "))

    def re_user(self):
        self.ls = []
        self.ls.append(Member.new_user(self))
        return self.ls

    def print_list(self):
        print("###회원 명단###")
        print("************************")
        print("아이디 비밀번호 이름")
        print("************************")
        [print(i) for i in self.ls]
        print("************************")


    def delete(self, ls, id):
        del self.ls[[i for i, j in enumerate(ls) if j.id == id][0]]

def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    ls = []
    t = Member('name', 'num', 'id')
    while True:
        menu = my_menu(MENUS)
        if menu == 0:
            print("종료")
            break
        else:
            try:
                member_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")



