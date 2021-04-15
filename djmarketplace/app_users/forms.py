from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""
    first_name = forms.CharField(max_length=30, required=False, label='First name')
    last_name = forms.CharField(max_length=30, required=False, label='Second name')
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')


class AddBalanceForm(forms.Form):
    """Форма для пополнения баланса пользователя"""
    amount = forms.IntegerField(required=True, label='Сумма пополнения', help_text='Укажите целое положительное число')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not isinstance(amount, int):
            raise ValidationError('Укажите целое положительное число!')
        if amount <= 0:
            raise ValidationError('Укажите целое положительное число!')
        return amount
