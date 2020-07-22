from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name ='home'),
    path('', views.json_fun),
    path('', views.lineChartData, name='chart_data'),
]