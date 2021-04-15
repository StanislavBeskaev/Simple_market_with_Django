from django.db import models
from django.urls import reverse


class HousingType(models.Model):
    """Модель для типа помещения"""
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип помещения'
        verbose_name_plural = 'Типы помещений'


class RoomsNumber(models.Model):
    """Модель для количества комнат"""
    name = models.CharField(max_length=50, verbose_name='Количество комнат')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Количество комнат'
        verbose_name_plural = 'Количества комнат'


class Housing(models.Model):
    """Модель жилья"""
    description = models.TextField(null=False, verbose_name='Описание')
    cost = models.PositiveIntegerField(verbose_name='Стоимость')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    housing_type = models.ForeignKey(HousingType, on_delete=models.CASCADE, verbose_name='Тип помещения')
    rooms_number = models.ForeignKey(RoomsNumber, on_delete=models.CASCADE, verbose_name='Количество комнат')
    created_date = models.DateField(null=False, verbose_name='Дата постройки/сдачи')
    is_sold = models.BooleanField(default=False, verbose_name='Флаг продано/непродано')

    class Meta:
        verbose_name = 'Жильё'
        verbose_name_plural = 'Жильё'

    def __str__(self):
        return f'{self.housing_type.name}, {self.rooms_number.name}, адрес: {self.address}; стоимость:{self.cost}'

    def get_absolute_url(self):
        return reverse('housing_detail', args=[str(self.id)])
