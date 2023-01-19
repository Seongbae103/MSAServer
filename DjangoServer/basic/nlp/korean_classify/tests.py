from basic.nlp.imdb.services import NaverMovieService

if __name__ == '__main__':
    # ImdbService().hook()
    result = NaverMovieService().process("평범한 영화. 무난하다")
    print(f"긍정률: {result}")
