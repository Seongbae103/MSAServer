from multiplex.randomlist import RandomList

class Bubble(object):
    def __init__(self):
        pass
    @staticmethod
    def bub_print():
        rl = RandomList().get_random(10, 100, 10)
        print(rl)
        for i in range(len(rl)-1):
            for j in range(len(rl)-1):
                if rl[j] > rl[j+1]:
                    rl[j], rl[j + 1] = rl[j+1], rl[j]
        print(rl)

if __name__ == '__main__':
    Bubble.bub_print()