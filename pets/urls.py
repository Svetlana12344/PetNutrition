from django.urls import path
from . import views

urlpatterns = [
    # Главная страница приложения pets
    path('', views.pet_list, name='pet_list'),

    # Добавление нового питомца
    path('add/', views.add_pet, name='add_pet'),

    # Просмотр деталей питомца
    path('<int:pet_id>/', views.pet_detail, name='pet_detail'),

    # Редактирование питомца
    path('<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),

    # Удаление питомца (будем добавлять позже)
    path('<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),

    # Поиск кормов через API
    path('food/search/', views.search_food_api, name='search_food_api'),

    # Импорт корма из API
    path('food/import/<int:food_id>/', views.import_food, name='import_food'),
]