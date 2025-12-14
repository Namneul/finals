from django.conf import settings
from django.db.models.expressions import result
from django.shortcuts import render, get_object_or_404
from .models import Restaurant
from .services import search_local_places

def home(request):
    return render(request, 'restaurants/home.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})

def restaurant_search(request):
    """
    네이버 지역 검색 API를 이용한 맛집 검색 페이지
    """

    query = request.GET.get("query", "")
    results = []

    if query:
        data = search_local_places(query=query, display=10, sort="random")
        if data and "items" in data:
            results = data["items"]

    context = {
        "query":query,
        "results":results,
    }
    return render(request, "restaurants/search.html", context)

def map_demo(request):
    return render(request, 'restaurants/map.html', {
        'NAVER_MAP_CLIENT_ID': settings.NAVER_MAP_CLIENT_ID,
    })

import json
from django.shortcuts import render
from .services import search_local_places


def nearby_restaurants(request):
    """
    /restaurants/nearby/?lat=...&lng=...&radius=...
    현재 위치 기준 주변 맛집 검색 (AJAX 없음, 전체 페이지 렌더링)
    """
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    radius = request.GET.get("radius", "1000")

    if not lat or not lng:
        return render(request, "restaurants/nearby.html", {
            "lat": None,
            "lng": None,
            "radius": radius,
            "places_json": "[]",
        })

    # 단순 예시: 현재는 query를 '맛집'으로 고정
    # 나중에 '한식', '카페' 같은 카테고리 옵션을 폼에서 받도록 확장 가능
    query = "맛집"

    places = search_local_places(query=query, display=10, sort="random")

    places_json = json.dumps(places, ensure_ascii=False)

    context = {
        "lat": lat,
        "lng": lng,
        "radius": radius,
        "places_json": places_json,
    }
    return render(request, "restaurants/nearby.html", context)
