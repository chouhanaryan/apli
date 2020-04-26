from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """ Movies model """

    title = models.CharField(max_length=50)
    youtube_link = models.CharField(max_length=150)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        """ String for representing the Movie model """
        return self.title


class Comment(models.Model):
    """ Comments model """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    text = models.TextField()

    def __str__(self):
        """ String for representing the Movie model """
        return self.user.username


class Preference(models.Model):
    """ Preference model """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ String for representing the Preference model """
        return str(self.user) + ":" + str(self.movie) + ":" + str(self.value)

    class Meta:
        unique_together = ("user", "movie", "value")
