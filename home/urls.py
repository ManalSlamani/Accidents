from django.urls import path
from . import views

urlpatterns = [
    path('', views.daybarchart, name='home'),
    path(r'get-data/', views.daybarchart, name='get-data'),
    # path(r'heatmap/?<int:myRadius>&<int:myOpacity>', views.makeHeatmap, name='heatmap'),
    # path(r'heatmap/', views.makeHeatmap, name='heatmap'),
    path(r'heatmap/', views.makeHeatmap, name='heatmap'),
    path(r'clustering/', views.makeClusters, name='clustering'),
    path(r'clustering/clusters/', views.makeClusters, name='clustering'),
    path(r'prediction/', views.makePrediction, name='prediction'),
    path(r'bdd/', views.allData, name='bdd')
]