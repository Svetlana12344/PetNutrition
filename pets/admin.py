from django.contrib import admin
from .models import Pet, Food


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'breed', 'age', 'weight', 'owner', 'created_at')
    list_filter = ('pet_type', 'activity_level', 'goal', 'created_at')
    search_fields = ('name', 'breed', 'owner__username')
    list_per_page = 20
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'pet_type', 'breed', 'owner')
        }),
        ('Физические параметры', {
            'fields': ('age', 'weight', 'activity_level')
        }),
        ('Цели и даты', {
            'fields': ('goal', 'created_at')
        }),
    )

    readonly_fields = ('created_at',)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'food_type', 'calories', 'protein', 'fat', 'price')
    list_filter = ('food_type', 'brand')
    search_fields = ('name', 'brand', 'suitable_for')
    list_editable = ('price',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'brand', 'food_type', 'price')
        }),
        ('Пищевая ценность', {
            'fields': ('calories', 'protein', 'fat', 'fiber')
        }),
        ('Дополнительно', {
            'fields': ('suitable_for',)
        }),
    )