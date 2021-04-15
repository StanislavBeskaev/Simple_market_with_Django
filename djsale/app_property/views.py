from django.views import generic

from .models import Housing


class HousingListView(generic.ListView):
    """Вью для страницы списка продаваемого жилья"""
    template_name = 'app_property/housing_list.html'
    model = Housing
    queryset = Housing.objects.filter(is_sold=False).select_related('housing_type', 'rooms_number')


class HousingDetailView(generic.DetailView):
    """Вью для детальной страницы жилья"""
    template_name = 'app_property/housing_detail.html'
    model = Housing
    queryset = Housing.objects.filter(is_sold=False).select_related('housing_type', 'rooms_number')
