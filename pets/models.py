from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
        ('rabbit', 'Кролик'),
        ('bird', 'Птица'),
        ('other', 'Другое'),
    ]

    GOALS = [
        ('weight_loss', 'Похудение'),
        ('weight_gain', 'Набор веса'),
        ('maintenance', 'Поддержание веса'),
        ('active', 'Активный образ жизни'),
        ('pregnant', 'Беременность/Лактация'),
    ]

    name = models.CharField(max_length=100, verbose_name="Кличка")
    pet_type = models.CharField(max_length=20, choices=PET_TYPES, verbose_name="Вид животного")
    breed = models.CharField(max_length=100, verbose_name="Порода", blank=True)
    age = models.IntegerField(verbose_name="Возраст (лет)")
    weight = models.FloatField(verbose_name="Вес (кг)")
    activity_level = models.CharField(max_length=20, choices=[
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ], verbose_name="Уровень активности")
    goal = models.CharField(max_length=20, choices=GOALS, verbose_name="Цель")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_pet_type_display()})"


class Food(models.Model):
    FOOD_TYPES = [
        ('dry', 'Сухой корм'),
        ('wet', 'Влажный корм'),
        ('natural', 'Натуральное питание'),
        ('mixed', 'Смешанное'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название корма")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES, verbose_name="Тип корма")
    calories = models.FloatField(verbose_name="Калорийность (ккал/100г)")
    protein = models.FloatField(verbose_name="Белок (%)")
    fat = models.FloatField(verbose_name="Жир (%)")
    fiber = models.FloatField(verbose_name="Клетчатка (%)")
    price = models.FloatField(verbose_name="Цена (руб/кг)", blank=True, null=True)
    suitable_for = models.CharField(max_length=100, verbose_name="Подходит для",
                                    help_text="Например: собаки крупных пород, котята")

    def __str__(self):
        return f"{self.brand} - {self.name}"
