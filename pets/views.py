from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pet, Food
from .forms import PetForm


def pet_list(request):
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
        'page_title': 'Все питомцы',
        'page_subtitle': f'Найдено {total_pets} питомцев',
    }
    return render(request, 'pets/pet_list.html', context)


def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Питомец "{pet.name}" добавлен!')
            return redirect('pet_list')
    else:
        form = PetForm()

    context = {
        'form': form,
        'page_title': 'Добавить питомца',
        'page_subtitle': 'Заполните информацию о питомце',
    }
    return render(request, 'pets/add_pet.html', context)


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.pet_type == 'dog':
        daily_calories = 30 * pet.weight + 70
    elif pet.pet_type == 'cat':
        daily_calories = 70 * (pet.weight ** 0.75)
    else:
        daily_calories = 50 * pet.weight

    context = {
        'pet': pet,
        'daily_calories': round(daily_calories),
        'protein_need': round(daily_calories * 0.03, 1),
        'fat_need': round(daily_calories * 0.01, 1),
        'page_title': f'Профиль: {pet.name}',
        'page_subtitle': f'{pet.get_pet_type_display()} | {pet.breed}',
    }
    return render(request, 'pets/pet_detail.html', context)