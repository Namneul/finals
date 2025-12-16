import re
import json
import requests
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from urllib.parse import quote
from .forms import PostForm, CommentForm

TAG_RE = re.compile(r"<[^>]+>")

def clean_text(v: str) -> str:
    return TAG_RE.sub("", v or "").strip()

def search_local_places(query, display=10, start=1, sort="random"):
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception:
        pass

    return []

def index(request):

    recent_posts = Post.objects.order_by('-created_at')[:4]

    return render(request, "restaurants/index.html", {
        'recent_posts': recent_posts
    })

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurants/list.html", {"restaurants": restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, "restaurants/detail.html", {"restaurant": restaurant})

def restaurant_search(request):
    raw_query = request.GET.get("query", "").strip()
    places_json = "[]"

    if raw_query:
        query = raw_query if ("맛집" in raw_query or "음식" in raw_query or "카페" in raw_query) else f"{raw_query} 맛집"
        items = search_local_places(query=query, display=10, start=1, sort="random")
        print("NAVER raw items =", len(items))

        places = []
        for it in items:
            title = clean_text(it.get("title", ""))
            if not title:
                continue

            category = it.get("category") or ""
            if category:
                category = category.split(">")[0]

            places.append({
                "title": title,
                "category": category,
                "address": it.get("address") or "",
                "roadAddress": it.get("roadAddress") or "",
                "telephone": it.get("telephone") or "",
                "link": it.get("link") or "",
                "mapx": it.get("mapx") or "",
                "mapy": it.get("mapy") or "",
            })

        places_json = json.dumps(places, ensure_ascii=False)

    return render(request, "restaurants/search.html", {
        "query": raw_query,
        "places_json": places_json,
        "NAVER_MAP_CLIENT_ID": settings.NAVER_MAP_CLIENT_ID,
    })

def search_api(request):
    raw_query = request.GET.get("query", "").strip()
    if not raw_query:
        return JsonResponse({"status": "error", "message": "query가 비었습니다."}, status=400)

    query = raw_query if ("맛집" in raw_query or "음식" in raw_query or "카페" in raw_query) else f"{raw_query} 맛집"
    items = search_local_places(query=query, display=10, start=1, sort="random")

    places = []
    for it in items:
        title = clean_text(it.get("title", ""))
        if not title:
            continue

        category = it.get("category") or ""
        if category:
            category = category.split(">")[0]

        places.append({
            "title": title,
            "category": category,
            "address": it.get("address") or "",
            "roadAddress": it.get("roadAddress") or "",
            "telephone": it.get("telephone") or "",
            "link": it.get("link") or "",
            "mapx": it.get("mapx") or "",
            "mapy": it.get("mapy") or "",
        })

    return JsonResponse({"status": "success", "places": places}, json_dumps_params={"ensure_ascii": False})

def roulette_view(request):
    return render(request, 'restaurants/roulette.html')

def roulette_search_api(request):
    food = request.GET.get('food')
    location = request.GET.get('location')

    if not food or not location:
        return JsonResponse({"status": "error", "message": "잘못된 요청입니다."})

    query = f"{location} {food}"

    items = search_local_places(query, display=30, sort='random')

    processed_places = []
    for item in items:
        title = item['title'].replace('<b>', '').replace('</b>', '')
        item['title'] = title
        if 'category' in item:
            item['category'] = item['category'].split('>')[0]
        processed_places.append(item)

    return JsonResponse({
        "status": "success",
        "places": processed_places,
        "search_query": query
    }, json_dumps_params={'ensure_ascii': False})


def board_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'restaurants/board_list.html', {'posts': posts})

def board_search_api(request):
    query = request.GET.get('query', '')
    if query:
        items = search_local_places(query, display=5)
        results = []
        for item in items:
            title = item['title'].replace('<b>', '').replace('</b>', '')
            results.append({
                'title': title,
                'category': item.get('category', '음식점'),
                'address': item.get('roadAddress') or item.get('address'),
                'link': item.get('link', '') or f"https://map.naver.com/v5/search/{title}"
            })
        return JsonResponse({'status': 'success', 'items': results})
    return JsonResponse({'status': 'fail'})


@login_required(login_url='login')
def board_write(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'restaurants/board_write.html', {'form': form})


def board_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:  # 비로그인 댓글 방지
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # ★ 댓글 작성자도 로그인 유저로
            comment.save()
            return redirect('board_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'restaurants/board_detail.html', {
        'post': post,
        'form': form
    })