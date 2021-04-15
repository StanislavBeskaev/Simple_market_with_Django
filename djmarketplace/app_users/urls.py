from django.urls import path

from . import views


urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),  # страница авторизации
    path('logout', views.LogoutView.as_view(), name='logout'),  # страница выхода
    path('register', views.register_view, name='register'),  # страница регистрации
    path('account', views.UserAccountView.as_view(), name='account'),  # Личный кабинет пользователя
    path('add_balance', views.AddBalanceView.as_view(), name='add_balance')  # страница пополнения баланса

]
