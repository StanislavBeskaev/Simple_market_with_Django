import random
import os
from loguru import logger

from django.contrib.auth.models import User
from django.db import transaction

from app_users import models
from djmarketplace.settings import BASE_DIR


my_format = '{level} {time} {name} {message}'

loguru_register_logger = logger.bind(name='register')
logger.add(sink=os.path.join(BASE_DIR, 'logs', 'registers.log'), format=my_format, level='INFO',
           filter=lambda record: record["extra"].get("name") == "register")

loguru_user_status_logger = logger.bind(name='user_status')
logger.add(sink=os.path.join(BASE_DIR, 'logs', 'user_status.log'), format=my_format, level='INFO',
           filter=lambda record: record["extra"].get("name") == "user_status")

loguru_balance_logger = logger.bind(name='balance')
logger.add(sink=os.path.join(BASE_DIR, 'logs', 'balance.log'), format=my_format, level='INFO',
           filter=lambda record: record["extra"].get("name") == "balance")

# Костанта для определения статуса пользователя в зависимости от суммы покупки
PROFILE_STATUSES_RANKING = [
    ('Золотой', 1000),
    ('Серебрянный', 100),
    ('Бронзовый', 0),
]

MIN_START_BALANCE = 0
MAX_START_BALANCE = 1000


def get_status_by_purchases_amount(amount: int) -> str:
    """Метод получения статуса по сумме покупок"""
    return_status = ''
    for status, purchases_amount in sorted(PROFILE_STATUSES_RANKING, key=lambda x: x[1]):
        if amount >= purchases_amount:
            return_status = status
    return return_status


@transaction.atomic
def refresh_status(user: User):
    """Метод обновляет информацию о статусе у пользователя user"""
    status_before_update = user.profile.status
    new_status = get_status_by_purchases_amount(user.profile.purchases_amount)
    if new_status != status_before_update:
        user.profile.status = new_status
        user.profile.save()
        loguru_user_status_logger.info(
            f'Пользователь {user.username}, изменение статуса с {status_before_update} на {new_status}')


def get_available_profile_statuses() -> list:
    """Метод получения списка доступных пользовательских статусов"""
    available_profile_statuses = [(entry[0], entry[0]) for entry in PROFILE_STATUSES_RANKING]
    return available_profile_statuses


def get_default_profile_status() -> str:
    """Метод получения начального пользовательского статуса"""
    for status, purchases_amount in PROFILE_STATUSES_RANKING:
        if purchases_amount == 0:
            return status


def create_profile_by_user(user: User):
    """Метод для создания профиля пользователя"""
    default_status = get_default_profile_status()
    balance = random.randint(MIN_START_BALANCE, MAX_START_BALANCE)
    models.Profile.objects.create(user=user,
                                  balance=balance,
                                  status=default_status
                                  )
    loguru_register_logger.info(f'Регистрация нового пользователя username={user.username}')
    loguru_user_status_logger.info(f'Пользователь {user.username}, создан со статусом {default_status}')
    loguru_balance_logger.info(f'Пользователь {user.username}, создан с балансом {balance}')


def add_balance_to_profile(profile, amount: int):
    """Метод для увеличения баланса пользователя"""
    profile.balance += amount
    profile.save()
    loguru_balance_logger.info(f'Пользователь: {profile.user.username}, пополнил баланс на {amount} баллов,'
                               f' текущий баланс {profile.balance}')


@transaction.atomic()
def buy_products_on_amount(user: User, amount: int):
    """Метод покупки товаров на сумму amount.
     Уменьшает баланс пользователя user на amount и увеличивает сумму покупок на amount"""
    user.profile.balance -= amount
    user.profile.purchases_amount += amount
    user.profile.save()
