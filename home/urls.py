from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('',views.home,name ='home'),
    path('', views.json_fun),
    """path('', views.lineChartData, name='chart_data'),"""
=======
    path('home/', views.home, name='home'),
    path(r'home/get-data/', views.get_data, name='get-data')
>>>>>>> 678fa17b156d2abb55bc202efcccd12bfdda8b28
]