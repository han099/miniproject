from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_num = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    class Meta:
        #db_table = 'posts' / 게시물에 대한 내림차순을 관리하는 속성을 지정
        ordering = ["-created_at"]

class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    # ForeignKey를 통해 댓글과 게시글 연결
    post = models.ForeignKey(Post, on_delete=models.CASCADE)




