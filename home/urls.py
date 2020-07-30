from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path(r'home/get-data/', views.get_data, name='get-data')
]