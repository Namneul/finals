from django.db import models
from django.conf import settings  # 유저 모델 가져오기 위해 필수
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=200)
    content = models.TextField()

    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True, verbose_name="음식 사진")

    res_name = models.CharField(max_length=100)
    res_address = models.CharField(max_length=200, blank=True)
    res_category = models.CharField(max_length=50, blank=True)
    res_link = models.URLField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:20]