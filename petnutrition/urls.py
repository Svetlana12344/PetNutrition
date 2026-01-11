from django.contrib import admin
from django.urls import path, include
from pets.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pets/', include('pets.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pets/', include('pets.urls')),
]