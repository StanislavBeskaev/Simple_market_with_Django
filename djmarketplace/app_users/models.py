from django.contrib.auth.models import User
from django.db import models

from services.users_services import get_available_profile_statuses


class Profile(models.Model):
    """Расширешие модели пользователя, для хранения баланса, текущего статуса, суммы покупок"""
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(verbose_name='Баланс')
    status = models.CharField(max_length=20, verbose_name='Статус', choices=get_available_profile_statuses())
    purchases_amount = models.PositiveIntegerField(default=0, verbose_name='Сумма покупок')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
