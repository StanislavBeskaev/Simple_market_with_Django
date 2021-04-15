import random

from app_product.models import Product, Store, Warehouse

TEST_PRODUCT_NAME_LIST = ['Ложка', 'Кружка', 'Вилка', 'Термос', 'Тарелка', 'Холодильник']
TEST_STORE_NAME_PREFIX = 'Магазин '
TEST_STORE_COUNT = 5
MIN_COUNT_STORE_PER_PRODUCT = 0
MAX_COUNT_STORE_PER_PRODUCT = 4
MIN_PRICE = 1
MAX_PRICE = 200
MIN_QUANTITY = 0
MAX_QUANTITY = 1000


def create_test_products():
    """Метод для создания тестовых товаров. Создаёт товары с названием из TEST_PRODUCT_NAME_LIST"""
    products_to_create = [Product(name=name) for name in TEST_PRODUCT_NAME_LIST]
    Product.objects.bulk_create(products_to_create)
    print(f'Создано {len(TEST_PRODUCT_NAME_LIST)} тестовых товаров')


def create_test_stores():
    """Метод для создания тестовых магазинов.
    Создаёт магазины с названием начинающимся на TEST_STORE_NAME_PREFIX + добавляется порядковый
    номер, начиная с 1,  в количестве TEST_STORE_COUNT штук"""
    stores_to_create = [Store(name=f'{TEST_STORE_NAME_PREFIX}{i+1}') for i in range(TEST_STORE_COUNT)]
    Store.objects.bulk_create(stores_to_create)
    print(f'Создано {TEST_STORE_COUNT} тестовых магазинов')


def create_test_warehouses():
    """Метод для создания тестовых складов.
    На каждый товар выбирается случайным образом магазины в количестве от MIN_COUNT_STORE_PER_PRODUCT
    до MAX_COUNT_STORE_PER_PRODUCT, со случайной ценой в диапозоне [MIN_PRICE, MAX_PRICE]
     и случайным количеством в диапазоне [MIN_QUANTITY, MAX_QUANTITY]"""
    exists_warehouses = list(Warehouse.objects.all())
    if len(exists_warehouses) > 0:
        print('Данные о складах уже есть, новые не будут созданы!')
        return
    products = list(Product.objects.all())
    if len(products) == 0:
        create_test_products()
        products = list(Product.objects.all())
    stores = list(Store.objects.all())
    if len(stores) == 0:
        create_test_stores()
        stores = list(Store.objects.all())
    warehouses_to_create = []
    counter = 0
    for product in products:
        count_stores_to_product = random.randint(MIN_COUNT_STORE_PER_PRODUCT, MAX_COUNT_STORE_PER_PRODUCT)
        random_stores = random.sample(stores, k=count_stores_to_product)
        for store in random_stores:
            new_warehouse = Warehouse(product=product,
                                      store=store,
                                      price=random.randint(MIN_PRICE, MAX_PRICE),
                                      quantity=random.randint(MIN_QUANTITY, MAX_QUANTITY)
                                      )
            warehouses_to_create.append(new_warehouse)
            counter += 1

    Warehouse.objects.bulk_create(warehouses_to_create)
    print(f'Создано {counter} тестовых складов')
