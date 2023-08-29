from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class MovieInfo(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    openingday = models.DateField()
    trailer = models.CharField(max_length=500)
    stillshot1 = models.ImageField(upload_to='images/', blank=True, null=True)
    stillshot2 = models.ImageField(upload_to='images/', blank=True, null=True)
    stillshot3 = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title


class MovieComment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    movie_id = models.ForeignKey('MovieInfo', on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    rating = models.IntegerField()
    update = models.DateTimeField(auto_now=True)  ## save시 자동으로

    class Meta:
        unique_together = ['user_id', 'movie_id']
        # 두개 합쳐서 유니크 키로 설정해준다... 쟝고에선 두개의 필드를 합쳐서 PK로 만드는 방법이 없으니 일반 pk 하나 설정해주고 유니크키 설정하는 방식으로
        # user_id와 movie_id를 유니크키 설정으로 한명이 커멘트 무한 작성하는것 방지용

    def __str__(self):
        return self.title
