from django.urls import path

from . import views


urlpatterns = [
    path('housing_list', views.HousingListView.as_view(), name='housing_list'),  # страница списка продаваемого жилья
    path('detail/<int:pk>', views.HousingDetailView.as_view(), name='housing_detail'),  # детальная страница жилья
]
