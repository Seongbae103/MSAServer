from datetime import datetime
import pytz

def current_time():
    tz = pytz.timezone('Asia/Seoul')
    cur_time = datetime.now(tz)
    current_time = cur_time.strftime("%H:%M:%S")
    return current_time
# return f"{datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')}"

def utc_seoul():
    return datetime.now(pytz.timezone('Asia/Seoul'))



if __name__ == '__main__':
    print(f"현재 서울 시간 : {utc_seoul()}")