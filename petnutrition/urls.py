from django.shortcuts import render
from django.contrib.auth.models import User
from pets.models import Pet, Food
from calculations.models import DietPlan

def home(request):
    context = {
        'pets_count': Pet.objects.count(),
        'foods_count': Food.objects.count(),
        'plans_count': DietPlan.objects.count(),
        'users_count': User.objects.count(),
    }
    return render(request, 'home.html', context)