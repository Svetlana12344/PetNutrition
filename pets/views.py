from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet, Food
from .forms import PetForm
from calculations.models import DietPlan, FoodRecommendation


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            create_diet_plan(pet)

            messages.success(
                request,
                f'Питомец "{pet.name}" добавлен! Создан план питания.'
            )
            return redirect('diet_plan', pet_id=pet.id)
    else:
        form = PetForm()

    return render(request, 'pets/add_pet.html', {'form': form})


def create_diet_plan(pet):
    if pet.pet_type == 'dog':
        daily_calories = 30 * pet.weight + 70
    elif pet.pet_type == 'cat':
        daily_calories = 70 * (pet.weight ** 0.75)
    else:
        daily_calories = 50 * pet.weight

    activity_multipliers = {
        'low': 1.2,
        'medium': 1.4,
        'high': 1.6
    }

    goal_multipliers = {
        'weight_loss': 0.8,
        'weight_gain': 1.2,
        'maintenance': 1.0,
        'active': 1.3,
        'pregnant': 1.5
    }

    final_calories = daily_calories * \
                     activity_multipliers.get(pet.activity_level, 1.4) * \
                     goal_multipliers.get(pet.goal, 1.0)

    diet_plan = DietPlan.objects.create(
        pet=pet,
        daily_calories=round(final_calories),
        protein_need=round(final_calories * 0.03, 1),
        fat_need=round(final_calories * 0.01, 1),
        is_active=True
    )

    recommend_foods(diet_plan)

    return diet_plan


def recommend_foods(diet_plan):
    pet = diet_plan.pet

    suitable_foods = Food.objects.filter(
        suitable_for__icontains=pet.get_pet_type_display()
    )[:3]

    for food in suitable_foods:
        daily_amount = (diet_plan.daily_calories / food.calories) * 100

        FoodRecommendation.objects.create(
            diet_plan=diet_plan,
            food=food,
            daily_amount=round(daily_amount),
            meal_count=2,
            notes=f"Автоматическая рекомендация для {pet.name}"
        )


@login_required
def diet_plan_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    try:
        diet_plan = DietPlan.objects.get(pet=pet, is_active=True)
        recommendations = FoodRecommendation.objects.filter(diet_plan=diet_plan)
    except DietPlan.DoesNotExist:
        diet_plan = create_diet_plan(pet)
        recommendations = FoodRecommendation.objects.filter(diet_plan=diet_plan)

    monthly_cost = 0
    for rec in recommendations:
        monthly_cost += (rec.daily_amount / 1000) * rec.food.price * 30

    context = {
        'pet': pet,
        'diet_plan': diet_plan,
        'recommendations': recommendations,
        'monthly_cost': round(monthly_cost, 2),
        'page_title': f'План питания: {pet.name}',
        'page_subtitle': 'Рекомендации по кормлению',
    }
    return render(request, 'pets/diet_plan.html', context)