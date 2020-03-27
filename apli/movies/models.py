from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):

    ''' Movie model '''
    title = models.CharField(max_length=50)
    youtube_link = models.CharField(max_length=150)


class Comment(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE ,editable=False)
    text = models.TextField()