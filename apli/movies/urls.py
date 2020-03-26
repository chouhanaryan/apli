from django.urls import path
from .views import movie_list, movie_detail, signup

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('<int:pk>/', movie_detail, name='movie_detail'),
    path('accounts/signup/', signup, name='signup')
]