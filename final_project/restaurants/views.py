from django.shortcuts import render, get_object_or_404
from .models import Restaurant

def home(request):
    return render(request, 'restaurants/home.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})