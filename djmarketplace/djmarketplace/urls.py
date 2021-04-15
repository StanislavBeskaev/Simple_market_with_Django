from django.contrib import admin
from django.urls import path, include

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('app_users.urls')),
    path('products/', include('app_product.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
