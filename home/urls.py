from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'^api/data/$', views.get_data, name='api-data')
]