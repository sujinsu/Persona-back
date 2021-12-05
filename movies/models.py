from django.db import models
from django.conf import settings
from django.db.models.expressions import Col

# Create your models here.
class Movie(models.Model):
    api_id = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=300, blank=True)
    release_date = models.DateField(blank=True)
    hits = models.PositiveIntegerField(default=0)    # 조회수
    vote_average = models.FloatField(default=0)    # 평점
    vote_count = models.PositiveIntegerField(default=0)    # 평점 계산의 위한 투표 수
    # 해당 movie를 좋아하는 사람들/ movie_id 와 user_id를 M:N
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    # movie 가 지워지면 review도 지워지도록
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    # review를 작성한 user, user가 탈퇴해도 review는 남아있도록
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='wrtie_reviews')
    # 해당 review를 좋아하는 user들/ movie_id와 user_id를 M:N
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movie_reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Form(models.Model):
    api_id = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=300, blank=True)
    release_date = models.DateField(blank=True)
    hits = models.PositiveIntegerField(default=0)    # 조회수
    vote_average = models.FloatField(default=0)    # 평점
    vote_count = models.PositiveIntegerField(default=0)


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_collections")
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    movies = models.ManyToManyField(Movie, related_name='collections')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_collections')


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="tags")
