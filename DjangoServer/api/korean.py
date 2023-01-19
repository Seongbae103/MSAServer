'''
from konlpy.tag import Okt
okt = Okt()
okt.pos('삼성전자 글로벌센터 전자사업부', stem=True)
with open('admin/crawling/data/kr-Report_2018.txt','r',
          encoding='UTF-8') as f:
    texts = f.read()
print(texts)
'''