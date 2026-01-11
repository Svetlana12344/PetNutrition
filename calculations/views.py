from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pets.models import Pet


@login_required
def calculate_diet(request):
    if request.method == 'POST':
        # Здесь будет логика расчета
        pet_id = request.POST.get('pet_id')
        pet = Pet.objects.get(id=pet_id)

        # Формула расчета базового метаболизма для собак
        if pet.pet_type == 'dog':
            if pet.weight <= 10:
                rer = 70 * (pet.weight ** 0.75)  # Базовая формула
            else:
                rer = 30 * pet.weight + 70

        # Формула для кошек
        elif pet.pet_type == 'cat':
            rer = 70 * (pet.weight ** 0.75)

        # Коэффициент активности
        activity_multiplier = {
            'low': 1.2,
            'medium': 1.4,
            'high': 1.6
        }.get(pet.activity_level, 1.4)

        # Коэффициент цели
        goal_multiplier = {
            'weight_loss': 0.8,
            'weight_gain': 1.2,
            'maintenance': 1.0,
            'active': 1.3,
            'pregnant': 1.5
        }.get(pet.goal, 1.0)

        daily_calories = rer * activity_multiplier * goal_multiplier

        context = {
            'pet': pet,
            'daily_calories': round(daily_calories),
            'protein_need': round(daily_calories * 0.03),  # 30% от калорий
            'fat_need': round(daily_calories * 0.01),  # 10% от калорий
        }
        return render(request, 'calculations/result.html', context)

    # GET запрос - показать форму
    user_pets = Pet.objects.filter(owner=request.user)
    return render(request, 'calculations/calculator.html', {'pets': user_pets})