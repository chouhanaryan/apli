from django.urls import path
from .views import movie_list, movie_detail, signup, CreateMovieView


urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('create/', CreateMovieView.as_view(), name='create_movie'),
    path('<int:pk>/', movie_detail, name='movie_detail'),
    path('accounts/signup/', signup, name='signup')
]