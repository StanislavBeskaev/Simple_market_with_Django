from django.contrib import admin

from .models import Store, Product, Warehouse, Cart, PurchaseHistory


@admin.register(Store)
class AdminStore(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ['id', 'product', 'store', 'price', 'quantity']


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'store', 'price', 'quantity']


@admin.register(PurchaseHistory)
class AdminPurchaseHistory(admin.ModelAdmin):
    list_display = ['id', 'date', 'user', 'product', 'store', 'price', 'quantity']