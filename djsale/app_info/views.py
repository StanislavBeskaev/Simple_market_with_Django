from django.shortcuts import render


def contact_view(request):
    """Вью для страницы контактов"""
    return render(request, 'app_info/contacts.html', {})


def about_view(request):
    """Вью для страницы О нас"""
    return render(request, 'app_info/about.html', {})


def main_view(request):
    """Вью для главной страницы"""
    return render(request, 'app_info/main.html', {})