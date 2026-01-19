from django.shortcuts import render, redirect, get_object_or_404
from pets.models import Pet
from .charts import generate_weight_chart, generate_nutrition_chart, generate_calorie_comparison


def calculate_diet(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        pet = Pet.objects.get(id=pet_id)

        if pet.pet_type == 'dog':
            if pet.weight <= 10:
                rer = 70 * (pet.weight ** 0.75)
            else:
                rer = 30 * pet.weight + 70

        elif pet.pet_type == 'cat':
            rer = 70 * (pet.weight ** 0.75)

        activity_multiplier = {
            'low': 1.2,
            'medium': 1.4,
            'high': 1.6
        }.get(pet.activity_level, 1.4)

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
            'protein_need': round(daily_calories * 0.03),
            'fat_need': round(daily_calories * 0.01),
        }
        return render(request, 'calculations/result.html', context)

    user_pets = Pet.objects.filter(owner=request.user)
    return render(request, 'calculations/calculator.html', {'pets': user_pets})



def pet_statistics(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    weight_chart = generate_weight_chart(pet)

    if pet.pet_type == 'dog':
        calories = 30 * pet.weight + 70
    else:
        calories = 70 * (pet.weight ** 0.75)

    context = {
        'pet': pet,
        'weight_chart': weight_chart,
        'daily_calories': round(calories),
        'protein_need': round(calories * 0.03, 1),
        'fat_need': round(calories * 0.01, 1),
    }

    return render(request, 'calculations/statistics.html', context)



def dashboard(request):
    user_pets = Pet.objects.filter(owner=request.user)

    if user_pets:
        comparison_chart = generate_calorie_comparison(user_pets)
    else:
        comparison_chart = None

    context = {
        'pets': user_pets,
        'comparison_chart': comparison_chart,
        'total_pets': user_pets.count(),
    }

    return render(request, 'calculations/dashboard.html', context)
