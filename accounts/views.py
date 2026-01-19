from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard(request):
    from pets.models import Pet
    from calculations.models import DietPlan

    pets = Pet.objects.filter(owner=request.user)
    diet_plans = DietPlan.objects.filter(pet__owner=request.user, is_active=True)

    context = {
        'user': request.user,
        'pets_count': pets.count(),
        'active_plans': diet_plans.count(),
        'recent_pets': pets.order_by('-created_at')[:3],
    }

    return render(request, 'accounts/dashboard.html', context)


from django.shortcuts import render

# Create your views here.
