from django.urls import path
from .views import movie_list, movie_detail, signup, add_movie

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('add_movie/', add_movie),
    path('<int:pk>/', movie_detail, name='movie_detail'),
    path('accounts/signup/', signup, name='signup')
]