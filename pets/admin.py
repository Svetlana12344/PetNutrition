from django.contrib import admin
from .models import Pet, Food


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'age', 'weight', 'owner')
    list_filter = ('pet_type', 'activity_level', 'goal')
    search_fields = ('name', 'breed')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'food_type', 'calories', 'protein')
    list_filter = ('food_type', 'brand')
    search_fields = ('name', 'brand')


from django.contrib import admin

# Register your models here.
