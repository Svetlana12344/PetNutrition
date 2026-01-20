import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petnutrition.settings')
django.setup()

from pets.models import Food

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
        'name': 'Whiskas для взрослых кошек',
        'brand': 'Whiskas',
        'food_type': 'wet',
        'calories': 85,
        'protein': 10,
        'fat': 5,
        'fiber': 1.5,
        'price': 300,
        'suitable_for': 'Взрослые кошки, все породы'
    },
    {
        'name': 'Pedigree для собак',
        'brand': 'Pedigree',
        'food_type': 'dry',
        'calories': 320,
        'protein': 22,
        'fat': 12,
        'fiber': 3.5,
        'price': 800,
        'suitable_for': 'Собаки всех пород'
    },
]

created_count = 0
for food_data in foods_data:
    if not Food.objects.filter(name=food_data['name'], brand=food_data['brand']).exists():
        Food.objects.create(**food_data)
        created_count += 1
        print(f" Создан корм: {food_data['name']}")

print(f"\n Итого: создано {created_count} новых кормов")