import os
from loguru import logger

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from djmarketplace.settings import BASE_DIR
from services.product_services import get_cart_info_by_user, get_user_purchase_history
from .forms import RegisterForm, AddBalanceForm
from services.users_services import create_profile_by_user, add_balance_to_profile


my_format = '{level} {time} {name} {message}'
loguru_login_logout_logger = logger.bind(name='login_logout')
logger.add(sink=os.path.join(BASE_DIR, 'logs', 'login_logout.log'), format=my_format, level='INFO',
           filter=lambda record: record["extra"].get("name") == "login_logout")


class LoginView(LoginView):
    template_name = 'app_users/login.html'

    def get_success_url(self):
        loguru_login_logout_logger.info(f'Пользователь {self.request.user.username} авторизовался')
        return super().get_success_url()


class LogoutView(LogoutView):
    template_name = 'app_users/logout.html'

    def dispatch(self, request, *args, **kwargs):
        loguru_login_logout_logger.info(f'Пользователь {request.user.username} вышел из системы')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    """Вью для страницы регистрации"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_profile_by_user(user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # "сырой" пароль
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            loguru_login_logout_logger.info(f'Пользователь {user.username} авторизовался')
            return redirect(to='account')

    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, template_name='app_users/register.html', context=context)


class UserAccountView(TemplateView):
    template_name = 'app_users/account.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart_info_by_user(user=self.request.user)
        context['purchase_history'] = get_user_purchase_history(user=self.request.user)
        return context


class AddBalanceView(TemplateView):
    template_name = 'app_users/add_balance.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['form'] = AddBalanceForm()
        context['cart'] = get_cart_info_by_user(user=self.request.user)
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        add_balance_form = AddBalanceForm(request.POST)
        profile = request.user.profile
        if add_balance_form.is_valid():
            amount = add_balance_form.cleaned_data.get('amount')
            add_balance_to_profile(profile=profile, amount=amount)
            return redirect(to='account')
        else:
            context['form'] = add_balance_form

        return render(request, self.template_name, context)
