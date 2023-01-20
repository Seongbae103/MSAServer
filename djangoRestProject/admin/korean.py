from konlpy.tag import Okt
okt = Okt()
okt.pos('삼성전자 글로벌센터 전자사업부', stem=True)
with open(r'C:\Users\AIA\PycharmProjects\djangoRestProject\basic\nlp\samsung_report\kr-Report_2018.txt',
          encoding='UTF-8') as f:
    texts = f.read()
print(texts)