import requests
from django.conf import settings

NAVER_LOCAL_SEARCH_URL = "https://openapi.naver.com/v1/search/local.json"

def search_local_places(query, display=10, start=1, sort="random"):
    """
        네이버 '지역 검색' API를 사용해 장소 검색.
        :param query: 검색어 (예: '전주 맛집', '전주 라멘')
        :param display: 한 번에 가져올 결과 수 (1~5 기본, 최대 5~?? API 정책 참고)
        :param start: 페이징 시작 위치
        :param sort: 'random' 또는 'comment' (리뷰순) 등
        :return: 결과 JSON(dict) 또는 에러시 None
        """
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }

    params = {
        "query": query,
        "display":display,
        "start":start,
        "sort":sort,
    }

    response = requests.get(NAVER_LOCAL_SEARCH_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        print("NAVER API error", response.status_code, response.text)
        return None