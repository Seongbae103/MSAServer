import os
import platform
myos = platform.system()
root = r"C:\Users\AIA\PycharmProjects\djangoRestProject"
def dir_path(param):
    if (param == "algorithms") :
        return os.path.join(root, "basic", param)
    elif (param == "aitrater") \
            or (param == "fashion") \
            or (param == "fruits") \
            or (param == "iris") \
            or (param == "lstm") \
            or (param == "mnist") :
        return os.path.join(root, "basic", "dlearn", param)
    elif (param == "bicycle") \
            or (param == "crime") \
            or (param == "etc") \
            or (param == "midwest") \
            or (param == "mpg") \
            or (param == "oklahoma") \
            or (param == "stroke") \
            or (param == "titanic") :
        return os.path.join(root, "basic", "mlearn", param)
    elif (param == "imdb") \
            or (param == "samsung_report") :
        return os.path.join(root, "basic", "nlp", param)
    elif (param == "pythonic") :
        return os.path.join(root, "basic", param)
    elif (param == "cnn") \
            or (param == "mosaic"):
        return os.path.join(root, "basic", "vision", param)
    elif (param == "webcrawler") :
        return os.path.join(root, "basic", param)
    elif (param == "krx") \
            or (param == "music")\
            or (param == "naver_movie"):
        return os.path.join(root, "basic", "webcrawler", param)
    elif (param == "b_comments") \
            or (param == "b_posts") \
            or (param == "b_tags") \
            or (param == "b_users") \
            or (param == "b_views"):
        return os.path.join(root, "blog", param)
    elif (param == "m_cinmas") \
            or (param == "m_movies") \
            or (param == "m_showtimes") \
            or (param == "m_theater_tickets") \
            or (param == "m_theaters"):
        return os.path.join(root, "multiplex", param)
    elif (param == "users") \
            or (param == "posts") :
        return os.path.join(root, "security", param)
    elif (param == "s_carts") \
            or (param == "s_categories") \
            or (param == "s_deliveries") \
            or (param == "s_orders") \
            or (param == "s_products") \
            or (param == "s_users") :
        return os.path.join(root, "shop", param)

if __name__ == '__main__':
    print(">> "+dir_path("s_carts"))