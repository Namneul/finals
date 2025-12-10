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