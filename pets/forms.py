from django import forms
from .models import Pet, Food


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'breed', 'age', 'weight', 'activity_level', 'goal']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Барсик, Шарик',
                'autofocus': True
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Сиамская, Лабрадор'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 30,
                'step': 1
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'placeholder': 'В кг'
            }),
            'pet_type': forms.Select(attrs={'class': 'form-select'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
        }

        labels = {
            'name': 'Кличка питомца',
            'pet_type': 'Вид животного',
            'breed': 'Порода',
            'age': 'Возраст (лет)',
            'weight': 'Вес (кг)',
            'activity_level': 'Уровень активности',
            'goal': 'Цель',
        }

        help_texts = {
            'weight': 'Укажите текущий вес питомца в килограммах',
            'activity_level': 'Насколько активен ваш питомец?',
            'goal': 'Какую цель вы преследуете?',
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Вес должен быть положительным числом")
        if weight > 100:
            raise forms.ValidationError("Вес не может превышать 100 кг")
        return weight

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Возраст не может быть отрицательным")
        if age > 30:
            raise forms.ValidationError("Возраст не может превышать 30 лет")
        return age

    def clean(self):
        cleaned_data = super().clean()
        pet_type = cleaned_data.get('pet_type')
        weight = cleaned_data.get('weight')

        if pet_type == 'cat' and weight and weight > 15:
            self.add_error('weight', "Кошки редко весят больше 15 кг. Проверьте данные.")

        if pet_type == 'dog' and cleaned_data.get('breed', '').lower() in ['чихуахуа', 'йорк', 'тойтерьер']:
            if weight and weight > 5:
                self.add_error('weight', "Для мелкой породы вес кажется слишком большим")

        return cleaned_data


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'brand', 'food_type', 'calories', 'protein', 'fat', 'fiber', 'price', 'suitable_for']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название корма'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бренд'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'protein': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Процент белка'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Процент жира'}),
            'fiber': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Процент клетчатки'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Цена за кг'}),
            'suitable_for': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Для кого подходит корм?'}),
            'food_type': forms.Select(attrs={'class': 'form-select'}),
        }

        labels = {
            'name': 'Название корма',
            'brand': 'Производитель',
            'food_type': 'Тип корма',
            'calories': 'Калорийность (ккал/100г)',
            'protein': 'Белок (%)',
            'fat': 'Жиры (%)',
            'fiber': 'Клетчатка (%)',
            'price': 'Цена (руб/кг)',
            'suitable_for': 'Подходит для',
        }