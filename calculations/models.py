from django.db import models
from pets.models import Pet, Food


class DietPlan(models.Model):
    """План питания"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="Питомец")
    daily_calories = models.FloatField(verbose_name="Суточная норма калорий")
    protein_need = models.FloatField(verbose_name="Потребность в белке (г)")
    fat_need = models.FloatField(verbose_name="Потребность в жирах (г)")
    recommended_foods = models.ManyToManyField(Food, through='FoodRecommendation',
                                               verbose_name="Рекомендуемые корма")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный план")

    def __str__(self):
        return f"План питания для {self.pet.name}"


class FoodRecommendation(models.Model):
    """Рекомендация по корму"""
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    daily_amount = models.FloatField(verbose_name="Суточная норма (г)")
    meal_count = models.IntegerField(verbose_name="Количество кормлений", default=2)
    notes = models.TextField(verbose_name="Примечания", blank=True)


from django.db import models

# Create your models here.
