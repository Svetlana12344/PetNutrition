from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.views.generic import RedirectView

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pets/', include('pets.urls')),
    path('', home, name='home'),
    path('add/', RedirectView.as_view(pattern_name='add_pet'), name='add_redirect'),
]