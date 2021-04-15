import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import generic

from services.product_services import get_product_list_with_stores, add_products_to_user_cart, get_cart_info_by_user, \
    get_cart_by_user, process_user_purchase, get_most_sold_products, COUNT_MOST_SOLD_PRODUCTS_TO_DISPLAY
from .forms import AddCountProductForm, SearchProductsForm
from .models import Product, Warehouse, Cart


class ProductListView(generic.ListView):
    """Вью для отображения списка товаров с магазинами, где эти товары есть"""
    template_name = 'app_product/product_list.html'
    model = Product
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = get_product_list_with_stores()
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['cart'] = get_cart_info_by_user(user=self.request.user)

        return context


class AddProductToCartView(generic.DetailView):
    """Вью для добавления товара в корзину"""
    model = Warehouse
    context_object_name = 'warehouse'
    template_name = 'app_product/add_product_to_cart.html'
    queryset = Warehouse.objects.select_related('product', 'store').all()

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        context = super().get_context_data(**kwargs)
        context['form'] = AddCountProductForm()
        context['cart'] = get_cart_info_by_user(user=self.request.user)
        return context

    def post(self, request, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        message = ''
        add_count_product_form = AddCountProductForm(request.POST)
        warehouse = self.get_object()
        if add_count_product_form.is_valid():
            product_count = add_count_product_form.cleaned_data['count']

            message = add_products_to_user_cart(user=request.user, warehouse=warehouse,
                                                product_count=product_count)
        context = {self.context_object_name: warehouse, 'form': add_count_product_form, 'message': message,
                   'cart': get_cart_info_by_user(user=request.user)}

        return render(self.request, self.template_name, context)


class CartView(generic.ListView):
    """Вью для отображения корзины пользователя"""
    template_name = 'app_product/cart.html'
    model = Cart
    context_object_name = 'product_list'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        queryset = get_cart_by_user(self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        context = super().get_context_data(**kwargs)

        context['cart'] = get_cart_info_by_user(user=self.request.user)

        return context

    def post(self, request):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        user = self.request.user
        user_balance = user.profile.balance
        context = {'cart': get_cart_info_by_user(user=user)}
        cart_price = context['cart'].get('price')

        if user_balance < cart_price:
            context['message'] = 'Не достаточно средств на балансе!'
            context['product_list'] = self.get_queryset()
            return render(request, self.template_name, context)

        else:
            process_user_purchase(user=user)
            return redirect(to='account')


class MostSoldProductReportView(generic.TemplateView):
    template_name = 'app_product/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchProductsForm()
        context['count'] = COUNT_MOST_SOLD_PRODUCTS_TO_DISPLAY
        if self.request.user.is_authenticated:
            context['cart'] = get_cart_info_by_user(user=self.request.user)
        return context

    def post(self, request):
        search_products_form = SearchProductsForm(request.POST)
        context = {'form': search_products_form, 'count': COUNT_MOST_SOLD_PRODUCTS_TO_DISPLAY}
        if search_products_form.is_valid():
            start = datetime.datetime.strptime(request.POST.get('start_datetime'), '%Y-%m-%dT%H:%M')
            end = datetime.datetime.strptime(request.POST.get('end_datetime'), '%Y-%m-%dT%H:%M')
            context['products'] = get_most_sold_products(start=start, end=end)
            context['report'] = True

        return render(request, self.template_name, context)
