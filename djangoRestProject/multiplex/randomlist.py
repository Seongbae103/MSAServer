import random


class RandomList(object):
    def __init__(self):
        pass

    def get_random(self, start, end, count):
        return random.sample(range(start, end), k = count)

    def print(self):
        print(self.get_random(1, 100, 10))


if __name__ == '__main__':
        rl = RandomList()
        rl.print()

