from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    """Главная страница"""
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pets/', include('pets.urls')),
    path('', home, name='home'),
]