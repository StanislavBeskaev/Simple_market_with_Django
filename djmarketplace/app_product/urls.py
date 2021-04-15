from django.urls import path

from . import views


urlpatterns = [
    path('product_list', views.ProductListView.as_view(), name='product_list'),  # страница со списком товаров и магазинов, где эти товары есть
    path('add_product_to_cart/<int:pk>', views.AddProductToCartView.as_view(), name='add_product_to_cart'),  # Страница добавления товара в корзину
    path('cart', views.CartView.as_view(), name='cart'),  # страница содержимого корзины
    path('most_sold_products', views.MostSoldProductReportView.as_view(), name='most_sold_products'),  # Страница отчёта наиболее продаваемых товаров
]
