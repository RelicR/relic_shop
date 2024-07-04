from django.urls import path
from . import views, api

app_name = 'relicshop'
urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('city/', api.GetCityList.as_view()),
    path('city/<int:city_id>/', api.GetCityName.as_view()),
    path('city/<int:city_id>/update/', api.SetCityStreets.as_view()),
    path('city/<int:city_id>/street/', api.GetCityStreets.as_view()),
    path('shop/', api.HandleShop.as_view()),
]