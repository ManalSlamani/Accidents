from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'get-data/', views.daybarchart, name='get-data'),
    path(r'heatmap/', views.makeHeatmap, name='heatmap')
]