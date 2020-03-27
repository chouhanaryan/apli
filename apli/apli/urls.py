from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),    # to include login/logout urls
    path('', include('movies.urls'))                           # to include movies app urls
]