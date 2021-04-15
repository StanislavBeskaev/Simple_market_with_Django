import datetime
import logging
import os

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Sum
from loguru import logger

from app_product.models import Product, Warehouse, Cart, PurchaseHistory
from djmarketplace.settings import BASE_DIR
from services.users_services import refresh_status, buy_products_on_amount

my_format = '{level} {time} {name} {message}'

loguru_balance_logger = logger.bind(name='balance')

loguru_purchase_logger = logger.bind(name='purchase')
logger.add(sink=os.path.join(BASE_DIR, 'logs', 'purchase.log'), format=my_format, level='INFO',
           filter=lambda record: record["extra"].get("name") == "purchase")

COUNT_MOST_SOLD_PRODUCTS_TO_DISPLAY = 5


def get_product_list_with_stores() -> list:
    """Метод получения списка товаров.
     К каждому товару добавляется атрибут warehouse_list, являющийся списком записей из Warehouse по этому товару"""
    product_list = Product.objects.all()
    warehouse_list = Warehouse.objects.filter(product__in=product_list).select_related('product', 'store').filter(quantity__gt=0)
    for product in product_list:
        store_price_quantity_list = []
        for warehouse in warehouse_list:
            if warehouse.product == product:
                store_price_quantity_list.append(warehouse)
        product.warehouse_list = store_price_quantity_list

    return product_list


@transaction.atomic
def add_products_to_user_cart(user: User, warehouse: Warehouse, product_count: int) -> str:
    """Метод добавления продуктов со склада Warehouse в корзину пользователя user в количестве product_count.
    Возвращает строку-сообщение об успехе/ неуспехе"""
    if warehouse.quantity < product_count:
        return 'Укажите количество товара не больше, чем есть на складе'

    user_cart = Cart.objects.filter(user=user, product=warehouse.product, store=warehouse.store) \
        .select_related('product', 'store').first()
    if user_cart:  # если в корзине уже есть этот товар из этого магазина, то добавляем нужное количество в корзину
        user_cart.quantity += product_count
        warehouse.quantity -= product_count
        user_cart.save()
        warehouse.save()
    else:  # если в корзине нет этого товара из этого магазина, то создаём новую запись
        Cart.objects.create(user=user,
                            product=warehouse.product,
                            store=warehouse.store,
                            price=warehouse.price,
                            quantity=product_count)
        warehouse.quantity -= product_count
        warehouse.save()

    return f'Товар в количестве {product_count} штук успешно добавлен в корзину'


def get_cart_info_by_user(user: User):
    """Метод получения корзины пользователя. Возращает словарь с ключами
     price - общая стоимость товаров в корзине
     quantity - общее количество товаров в корзине
     """
    return_dict = {}
    cart_entries = list(Cart.objects.filter(user=user))
    total_price = 0
    total_quantity = 0
    if cart_entries:
        for cart_entry in cart_entries:
            total_price += cart_entry.price * cart_entry.quantity
            total_quantity += cart_entry.quantity
        return_dict['price'] = total_price
        return_dict['quantity'] = total_quantity
    return return_dict


def get_cart_by_user(user: User):
    """Метод получения корзины пользоваетеля. Возврщает queryset из объектов Cart"""
    return Cart.objects.filter(user=user).select_related('product', 'store')


def delete_user_cart(user: User):
    """Метод удаления товаров из корзины пользователя user"""
    Cart.objects.filter(user=user).delete()


@transaction.atomic
def process_user_purchase(user: User):
    """Метод осуществления покупки товаров из корзины пользователя user"""
    cart_list = list(get_cart_by_user(user))
    cart_price = get_cart_info_by_user(user).get('price')
    loguru_purchase_logger.info(f'Пользователь {user.username} оформил заказ на сумму {cart_price}')
    create_purchases_to_history_from_cart(cart_list)
    delete_user_cart(user)
    buy_products_on_amount(user=user, amount=cart_price)
    loguru_balance_logger.info(f'Пользователь: {user.username}, списание {cart_price} баллов с баланса,'
                               f' текущий баланс {user.profile.balance} ')
    refresh_status(user)


@transaction.atomic()
def create_purchases_to_history_from_cart(cart_list: list):
    """Метод создаёт покупки в истории покупок PurchaseHistory из списка cart_list"""
    purchase_history_list_to_create = []
    for cart_entry in cart_list:
        purchase = PurchaseHistory(
            date=datetime.datetime.now(),
            user=cart_entry.user,
            product=cart_entry.product,
            store=cart_entry.store,
            price=cart_entry.price,
            quantity=cart_entry.quantity)
        loguru_purchase_logger.info(f'Покупка товаров: {cart_entry}')
        purchase_history_list_to_create.append(purchase)
    PurchaseHistory.objects.bulk_create(purchase_history_list_to_create)


def get_user_purchase_history(user: User):
    """Метод получения истории покупок пользователя user.
     Возращает queryset упорядоченный по дате покупки по убыванию"""
    return list(PurchaseHistory.objects.filter(user=user).select_related('product', 'store').order_by('-date'))


def get_most_sold_products(start: datetime, end: datetime):
    """Метод получения наиболее продаваемых товаров за период времени между start и end"""
    products = PurchaseHistory.objects.filter(date__gte=start).filter(date__lte=end).select_related('product')
    products = products.annotate(product_name=F('product__name')).values('product', 'product_name'). \
                   annotate(sum_quantity=Sum('quantity')).order_by('-sum_quantity')[
               :COUNT_MOST_SOLD_PRODUCTS_TO_DISPLAY]

    return list(products)
