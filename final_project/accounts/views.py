from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from restaurants.models import Post

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url='login')
def profile_view(request):
    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'my_posts': my_posts
    })