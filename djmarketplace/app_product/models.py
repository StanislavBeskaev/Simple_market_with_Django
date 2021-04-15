import datetime

from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    """Модель для хранения информации о магазинах"""
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель для хранения информации о товаре"""
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """Модель склада товаров. Показывает информацию о товарах в магазинах"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Магазин')
    price = models.PositiveIntegerField(verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')

    class Meta:
        verbose_name = 'Склад товара'
        verbose_name_plural = 'Склады товаров'
        unique_together = ('product', 'store')

    def __str__(self):
        return f'Товар: {self.product.name}; Магазин: {self.store.name}; Цена: {self.price}; ' \
               f'Количество товара: {self.quantity} '


class Cart(models.Model):
    """Модель корзины пользователя.
    Содержит информацию о пользователе, товаре, магазине товара, цене и количестве покупаемого товара"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Магазин')
    price = models.PositiveIntegerField(verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'

    def __str__(self):
        return f'Пользователь: {self.user.username}, товар: {self.product.name}, магазин: {self.store.name}, ' \
               f'цена: {self.price}, количество: {self.quantity}'


class PurchaseHistory(models.Model):
    """Модель для хранения истории покупок товаров"""
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата покупки')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, verbose_name='Магазин')
    price = models.PositiveIntegerField(verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'История покупок'

    def __str__(self):
        return f'Дата: {self.date}, Пользователь: {self.user.username}, товар: {self.product.name},' \
               f' магазин: {self.store.name}, цена: {self.price}, количество: {self.quantity}'
