from django import forms
from django.core.exceptions import ValidationError


class AddCountProductForm(forms.Form):
    """Форма для выбора количества товара для добавления к корзину"""
    count = forms.IntegerField(required=True, label='Количество товара')

    def clean_count(self):
        count = self.cleaned_data['count']
        if not isinstance(count, int):
            raise ValidationError('Укажите целое положительное число!')
        if count <= 0:
            raise ValidationError('Укажите целое положительное число!')
        return count


class SearchProductsForm(forms.Form):
    """Форма для поиска наиболее продаваемых товаров за период"""
    start_datetime = forms.DateTimeField(label='Дата и время начала', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(label='Дата и время конца', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
