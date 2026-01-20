"""from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
    path('<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),
    path('food/search/', views.search_food_api, name='search_food_api'),
    path('food/import/<int:food_id>/', views.import_food, name='import_food'),
    path('admin-demo/', views.admin_demo, name='admin_demo'),
]"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('<int:pet_id>/diet-plan/', views.diet_plan_view, name='diet_plan'),
]