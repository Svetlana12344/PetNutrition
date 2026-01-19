import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petnutrition.settings')

django.setup()

from django.contrib.auth.models import User
from pets.models import Pet, Food
from calculations.models import DietPlan, FoodRecommendation


def create_admin_and_data():
    print("=" * 50)
    print("Создание администратора и тестовых данных")
    print("=" * 50)

    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@petnutrition.ru',
            password='admin123'
        )
        print(f" Создан администратор: {admin_user.username}")
    except Exception as e:
        admin_user = User.objects.get(username='admin')
        print(f"ℹ Администратор уже существует: {admin_user.username}")

    try:
        demo_user = User.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='demo123'
        )
        print(f" Создан демо-пользователь: {demo_user.username}")
    except Exception as e:
        demo_user = User.objects.get(username='demo')
        print(f"ℹ Демо-пользователь уже существует: {demo_user.username}")

    foods_data = [
        {
            'name': 'Royal Canin для взрослых собак',
            'brand': 'Royal Canin',
            'food_type': 'dry',
            'calories': 350,
            'protein': 26,
            'fat': 16,
            'fiber': 2.5,
            'price': 1200,
            'suitable_for': 'Собаки старше 1 года'
        },
        {
            'name': 'Purina Pro Plan для кошек',
            'brand': 'Purina',
            'food_type': 'dry',
            'calories': 380,
            'protein': 34,
            'fat': 18,
            'fiber': 3.0,
            'price': 1500,
            'suitable_for': 'Кошки с чувствительным пищеварением'
        },
        {
            'name': 'Acana для щенков',
            'brand': 'Acana',
            'food_type': 'dry',
            'calories': 390,
            'protein': 33,
            'fat': 20,
            'fiber': 2.8,
            'price': 1800,
            'suitable_for': 'Щенки'
        },
        {
            'name': 'Whiskas влажный корм',
            'brand': 'Whiskas',
            'food_type': 'wet',
            'calories': 85,
            'protein': 10,
            'fat': 5,
            'fiber': 1.5,
            'price': 300,
            'suitable_for': 'Взрослые кошки'
        },
    ]

    created_foods = []
    for food_data in foods_data:
        food, created = Food.objects.get_or_create(
            name=food_data['name'],
            brand=food_data['brand'],
            defaults=food_data
        )
        if created:
            created_foods.append(food.name)
            print(f" Создан корм: {food.name}")

    pets_data = [
        {
            'name': 'Барсик',
            'pet_type': 'cat',
            'breed': 'Британский',
            'age': 3,
            'weight': 5.0,
            'activity_level': 'medium',
            'goal': 'maintenance',
            'owner': demo_user
        },
        {
            'name': 'Шарик',
            'pet_type': 'dog',
            'breed': 'Лабрадор',
            'age': 5,
            'weight': 25.0,
            'activity_level': 'high',
            'goal': 'weight_loss',
            'owner': demo_user
        },
        {
            'name': 'Мурка',
            'pet_type': 'cat',
            'breed': 'Сиамская',
            'age': 2,
            'weight': 3.5,
            'activity_level': 'low',
            'goal': 'weight_gain',
            'owner': demo_user
        },
        {
            'name': 'Рекс',
            'pet_type': 'dog',
            'breed': 'Овчарка',
            'age': 4,
            'weight': 30.0,
            'activity_level': 'high',
            'goal': 'active',
            'owner': demo_user
        },
    ]

    created_pets = []
    for pet_data in pets_data:
        pet, created = Pet.objects.get_or_create(
            name=pet_data['name'],
            owner=pet_data['owner'],
            defaults=pet_data
        )
        if created:
            created_pets.append(pet.name)
            print(f" Создан питомец: {pet.name}")

            if pet.pet_type == 'dog':
                daily_calories = 30 * pet.weight + 70
            else:
                daily_calories = 70 * (pet.weight ** 0.75)

            diet_plan = DietPlan.objects.create(
                pet=pet,
                daily_calories=round(daily_calories),
                protein_need=round(daily_calories * 0.03, 1),
                fat_need=round(daily_calories * 0.01, 1),
                is_active=True
            )
            print(f"  Создан план питания: {diet_plan.daily_calories} ккал/день")

    print("\n" + "=" * 50)
    print(" ИТОГОВАЯ СТАТИСТИКА:")
    print("=" * 50)
    print(f"Всего пользователей: {User.objects.count()}")
    print(f"Всего питомцев: {Pet.objects.count()}")
    print(f"Всего кормов: {Food.objects.count()}")
    print(f"Всего планов питания: {DietPlan.objects.count()}")

    print("\nДАННЫЕ ДЛЯ ВХОДА:")
    print("-" * 30)
    print("Администратор:")
    print("  Логин: admin")
    print("  Пароль: admin123")
    print("  Ссылка: /admin/")
    print("\nДемо-пользователь:")
    print("  Логин: demo")
    print("  Пароль: demo123")
    print("\nСсылка на админку: https://ваш-сайт/admin/")
    print("=" * 50)


if __name__ == "__main__":
    create_admin_and_data()