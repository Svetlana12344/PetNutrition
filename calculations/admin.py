from django.contrib import admin
from .models import DietPlan, FoodRecommendation


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('pet', 'daily_calories', 'protein_need', 'fat_need', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('pet__name',)
    list_editable = ('is_active',)


@admin.register(FoodRecommendation)
class FoodRecommendationAdmin(admin.ModelAdmin):
    list_display = ('diet_plan', 'food', 'daily_amount', 'meal_count')
    list_filter = ('meal_count',)
    search_fields = ('diet_plan__pet__name', 'food__name')
