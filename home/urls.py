from django.urls import path
from . import views
from .views import ShowProfileView, UserEditView
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
    # path(r'predictor/', views.makePredictor, name='predictor'),
    path(r'bdd/', views.allData, name='bdd'),
    path(r'authentification/', views.authentification, name='authentif'),
    path(r'<int:pk>/profile/', ShowProfileView.as_view(), name='profile'),
    path(r'edit-profile/', UserEditView.as_view(), name='edition'),
    path(r'logout/', views.logoutUser, name='logout'),
    #path('register/',views.registerPage, name='register'),
    path(r'upload/', views.uploadData, name='upload'),
    path(r'change/', views.changeWilaya, name='change'),
    # path(r'bdd/', views.uploadData, name='bdd'),
    # path(r'bdd/', views.uploadData name='bdd'),
    path(r'help/', views.help, name='help'),

]