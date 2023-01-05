import googlemaps as googlemaps

if __name__ == '__main__':
    key = '키 입력(쓰면 지워라)'
    gmaps = googlemaps.Client(key=key)
    print(gmaps.geocode('대한민국 서울특별시 강남구 대치2동 514', language='ko'))