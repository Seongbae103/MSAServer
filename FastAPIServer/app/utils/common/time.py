from datetime import datetime
import pytz


def current_time():
    return f"{datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')}"

def utc_seoul():
    return datetime.now(pytz.timezone('Asia/Seoul'))


from datetime import datetime

from random import randrange
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def between_random_date():
    d1 = datetime.strptime('1988-1-1', '%Y-%m-%d')
    d2 = datetime.strptime('2005-12-31', '%Y-%m-%d')
    target = str(random_date(d1, d2))
    return target.split()[0]



if __name__ == '__main__':
    print(f"랜덤 생일 : {between_random_date()}")