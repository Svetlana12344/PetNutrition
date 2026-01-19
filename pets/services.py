import requests
import json
from django.conf import settings


class PetFoodAPI:
    """Класс для работы с API кормов для животных"""

    def __init__(self):
        self.base_url = "https://api.example.com"  # Замените на реальный URL
        self.api_key = getattr(settings, 'PETFOOD_API_KEY', 'demo-key')

    def search_food(self, query, pet_type=None):
        """Поиск корма по названию"""
        # Имитация API для демонстрации
        mock_foods = [
            {
                'id': 1,
                'name': 'Royal Canin для собак',
                'brand': 'Royal Canin',
                'type': 'dry',
                'calories': 350,
                'protein': 26,
                'fat': 16,
                'price': 1200,
                'description': 'Сбалансированный корм для взрослых собак'
            },
            {
                'id': 2,
                'name': 'Pro Plan для кошек',
                'brand': 'Purina Pro Plan',
                'type': 'dry',
                'calories': 380,
                'protein': 34,
                'fat': 18,
                'price': 1500,
                'description': 'Корм для кошек с чувствительным пищеварением'
            },
            {
                'id': 3,
                'name': 'Acana для щенков',
                'brand': 'Acana',
                'type': 'dry',
                'calories': 390,
                'protein': 33,
                'fat': 20,
                'price': 1800,
                'description': 'Беззерновой корм для щенков'
            }
        ]

        # Фильтрация по запросу
        results = []
        for food in mock_foods:
            if query.lower() in food['name'].lower():
                if pet_type:
                    # Здесь можно добавить логику фильтрации по типу животного
                    pass
                results.append(food)

        return results

    def get_food_details(self, food_id):
        """Получение детальной информации о корме"""
        # Имитация запроса к API
        all_foods = self.search_food("")
        for food in all_foods:
            if food['id'] == food_id:
                return food
        return None


# Функция для сохранения данных из API в базу
def import_food_from_api(food_data):
    """Сохраняет данные корма из API в нашу базу"""
    from .models import Food

    # Преобразуем типы корма
    food_type_mapping = {
        'dry': 'dry',
        'wet': 'wet',
        'canned': 'wet'
    }

    food, created = Food.objects.update_or_create(
        external_id=food_data.get('id'),
        defaults={
            'name': food_data.get('name'),
            'brand': food_data.get('brand'),
            'food_type': food_type_mapping.get(food_data.get('type'), 'dry'),
            'calories': food_data.get('calories', 0),
            'protein': food_data.get('protein', 0),
            'fat': food_data.get('fat', 0),
            'price': food_data.get('price'),
            'suitable_for': food_data.get('description', '')
        }
    )
    return food, created