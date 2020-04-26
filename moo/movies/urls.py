from django.urls import path
from .views import (
    movie_list,
    movie_detail,
    preference,
    signup,
    CreateMovieView,
    DeleteMovieView,
    comment_delete,
)


urlpatterns = [
    path("", movie_list, name="movie_list"),  # Main movie home page view
    path("accounts/signup/", signup, name="signup"),  # New users sign up view
    path(
        "<int:pk>/preference/<int:userpreference>/", preference, name="preference"
    ),  # Like/Dislike a movie
    path(
        "<int:pk>/delete/<int:commentid>/", comment_delete, name="comment_delete"
    ),  # Delete comment view
    path("<int:pk>/delete/", comment_delete, name="movie_delete"),  # Delete movie view
    path("<int:pk>/", movie_detail, name="movie_detail"),  # Detail movie view
    path(
        "create/", CreateMovieView.as_view(), name="create_movie"
    ),  # Create movie view
]
