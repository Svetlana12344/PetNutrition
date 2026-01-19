import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64
import pandas as pd
from datetime import datetime, timedelta
import random

matplotlib.use('Agg')

def generate_weight_chart(pet, days=30):
    dates = [(datetime.now() - timedelta(days=i)).date()
             for i in range(days, 0, -1)]

    base_weight = pet.weight
    weights = []
    current = base_weight

    for i in range(days):
        change = random.uniform(-0.2, 0.3)

        if pet.goal == 'weight_loss':
            trend = -0.05
        elif pet.goal == 'weight_gain':
            trend = 0.05
        else:
            trend = 0

        current += change + trend
        weights.append(round(current, 1))

    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linewidth=2, color='#2E86AB')

    plt.axhline(y=pet.weight, color='r', linestyle='--',
                label=f'Текущий вес: {pet.weight} кг')

    plt.title(f'Динамика веса {pet.name}', fontsize=14, fontweight='bold')
    plt.xlabel('Дата')
    plt.ylabel('Вес (кг)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return graphic


def generate_nutrition_chart(diet_plan):
    total = diet_plan.protein_need + diet_plan.fat_need + 50

    labels = ['Белки', 'Жиры', 'Углеводы']
    sizes = [
        diet_plan.protein_need,
        diet_plan.fat_need,
        50
    ]
    colors = ['#4ECDC4', '#FF6B6B', '#FFE66D']

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, shadow=True)
    plt.title('Соотношение БЖУ в рационе', fontsize=14)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return graphic


def generate_calorie_comparison(pets):
    pet_names = [pet.name for pet in pets]
    calories = []

    for pet in pets:
        if pet.pet_type == 'dog':
            calories_needed = 30 * pet.weight + 70
        else:  # cat
            calories_needed = 70 * (pet.weight ** 0.75)
        calories.append(round(calories_needed))

    plt.figure(figsize=(8, 5))
    bars = plt.bar(pet_names, calories, color=['#2E86AB', '#A23B72', '#F18F01'])

    for bar, value in zip(bars, calories):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                 f'{value} ккал', ha='center', va='bottom')

    plt.title('Сравнение суточной нормы калорий', fontsize=14)
    plt.ylabel('Калории (ккал/день)')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode('utf-8')