from django.urls import path
from .views import movie_list, movie_detail, signup, CreateMovieView, DeleteMovieView


urlpatterns = [
    path('', movie_list, name='movie_list'),                                    # Main movie home page view
    path('accounts/signup/', signup, name='signup'),                            # New users sign up view
    path('<int:pk>/delete/', DeleteMovieView.as_view(), name='delete_movie'),   # Delete movie view
    path('<int:pk>/', movie_detail, name='movie_detail'),                       # Detail movie view
    path('create/', CreateMovieView.as_view(), name='create_movie')             # Create new movie view (Modal)
]