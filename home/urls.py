from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.daybarchart, name='home'),
    path(r'get-data/', views.daybarchart, name='get-data'),
    # path(r'heatmap/?<int:myRadius>&<int:myOpacity>', views.makeHeatmap, name='heatmap'),
    # path(r'heatmap/', views.makeHeatmap, name='heatmap'),
    path(r'heatmap/', views.makeHeatmap, name='heatmap'),
    path(r'clustering/', views.makeClusters, name='clustering'),
    # path(r'clustering/clusters.html', 'clusters.html', name='clustering'),
    # (r'(.+\.html)$', 'clusters.html'),
    # path(r'clustering/clusters.html', TemplateView.as_view(template_name='home/clusters.html'), name='clusters'),
    path(r'prediction/', views.makePrediction, name='prediction'),
    path(r'bdd/', views.allData, name='bdd')
]