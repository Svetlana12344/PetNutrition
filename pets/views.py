from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet, Food
from .forms import PetForm, FoodForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            messages.success(
                request,
                f'Питомец "{pet.name}" успешно добавлен! '
                f'Теперь можно рассчитать его рацион питания.'
            )
            return redirect('pet_detail', pet_id=pet.id)
        else:
            messages.error(
                request,
                'Пожалуйста, исправьте ошибки в форме.'
            )
    else:
        form = PetForm()

    context = {
        'form': form,
        'page_title': 'Добавить нового питомца',
        'page_subtitle': 'Заполните информацию о вашем питомце',
    }
    return render(request, 'pets/add_pet.html', context)


@login_required
def pet_list(request):
    if request.user.is_authenticated:
        pets = Pet.objects.filter(owner=request.user).order_by('-created_at')
    else:
        pets = Pet.objects.all().order_by('-created_at')[:10]

    total_pets = pets.count()
    dogs_count = pets.filter(pet_type='dog').count()
    cats_count = pets.filter(pet_type='cat').count()
    other_count = total_pets - dogs_count - cats_count

    context = {
        'pets': pets,
        'total_pets': total_pets,
        'dogs_count': dogs_count,
        'cats_count': cats_count,
        'other_count': other_count,
        'page_title': 'Питомцы',
        'page_subtitle': f'Найдено {total_pets} питомцев',
    }
    return render(request, 'pets/pet_list.html', context)


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

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

    context = {
        'pet': pet,
        'daily_calories': round(final_calories),
        'protein_need': round(final_calories * 0.03, 1),
        'fat_need': round(final_calories * 0.01, 1),
        'page_title': f'Профиль: {pet.name}',
        'page_subtitle': f'{pet.get_pet_type_display()} | {pet.breed}',
    }
    return render(request, 'pets/pet_detail.html', context)


@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные питомца "{pet.name}" обновлены!')
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    context = {
        'form': form,
        'pet': pet,
        'page_title': f'Редактирование: {pet.name}',
        'page_subtitle': 'Измените необходимые данные',
    }
    return render(request, 'pets/edit_pet.html', context)


@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet_name = pet.name
    pet.delete()

    messages.success(request, f'Питомец "{pet_name}" удален.')
    return redirect('pet_list')


def search_food_api(request):
    query = request.GET.get('q', '')

    mock_foods = [
        {
            'id': 1,
            'name': 'Royal Canin для взрослых собак',
            'brand': 'Royal Canin',
            'calories': 350,
            'protein': 26,
            'fat': 16,
            'price': 1200,
            'description': 'Для собак старше 1 года'
        },
        {
            'id': 2,
            'name': 'Purina Pro Plan для кошек',
            'brand': 'Purina',
            'calories': 380,
            'protein': 34,
            'fat': 18,
            'price': 1500,
            'description': 'Для кошек с чувствительным пищеварением'
        },
        {
            'id': 3,
            'name': 'Acana для щенков',
            'brand': 'Acana',
            'calories': 390,
            'protein': 33,
            'fat': 20,
            'price': 1800,
            'description': 'Беззерновой корм для щенков'
        }
    ]

    results = []
    if query:
        for food in mock_foods:
            if query.lower() in food['name'].lower() or \
                    query.lower() in food['brand'].lower():
                results.append(food)
    else:
        results = mock_foods[:5]

    context = {
        'results': results,
        'query': query,
        'results_count': len(results),
        'page_title': 'Поиск кормов',
        'page_subtitle': 'Найдите подходящий корм для вашего питомца',
    }
    return render(request, 'pets/food_search.html', context)


@login_required
def import_food(request, food_id):
    mock_foods = {
        1: {
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
        2: {
            'name': 'Purina Pro Plan для кошек',
            'brand': 'Purina',
            'food_type': 'dry',
            'calories': 380,
            'protein': 34,
            'fat': 18,
            'fiber': 3.0,
            'price': 1500,
            'suitable_for': 'Кошки с чувствительным пищеварением'
        }
    }

    food_data = mock_foods.get(food_id)

    if food_data:
        food, created = Food.objects.update_or_create(
            name=food_data['name'],
            brand=food_data['brand'],
            defaults={
                'food_type': food_data['food_type'],
                'calories': food_data['calories'],
                'protein': food_data['protein'],
                'fat': food_data['fat'],
                'fiber': food_data['fiber'],
                'price': food_data['price'],
                'suitable_for': food_data['suitable_for']
            }
        )

        if created:
            messages.success(request, f'Корм "{food.name}" добавлен в базу!')
        else:
            messages.info(request, f'Корм "{food.name}" уже был в базе (обновлен).')

    return redirect('search_food_api')


@staff_member_required
def admin_demo(request):
    users_count = User.objects.count()
    pets_count = Pet.objects.count()
    foods_count = Food.objects.count()
    from calculations.models import DietPlan
    plans_count = DietPlan.objects.count()

    sample_pets = Pet.objects.all().order_by('?')[:5]
    sample_foods = Food.objects.all().order_by('?')[:5]

    context = {
        'users_count': users_count,
        'pets_count': pets_count,
        'foods_count': foods_count,
        'plans_count': plans_count,
        'sample_pets': sample_pets,
        'sample_foods': sample_foods,
        'page_title': 'Демо: Админка и тестовые данные',
        'page_subtitle': 'Демонстрация работы системы администрирования',
    }
    return render(request, 'admin_demo.html', context)
