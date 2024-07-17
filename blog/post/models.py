from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    auther = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_index=True)
    created = models.DateField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, db_index=True, related_name="comments")
    auther = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_index=True)
    created = models.DateField(auto_now_add=True)
