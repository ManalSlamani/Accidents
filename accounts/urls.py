from django.conf.urls import url,include
from django.urls import path
from . import views
#from accounts.views import dashboard

urlpatterns = [
    # path('', views.dashboard, name="dashboard"),
      url(r"^accounts/", include("django.contrib.auth.urls")),
      url(r"^dashboard/", views.dashboard, name="dashboard"),

]