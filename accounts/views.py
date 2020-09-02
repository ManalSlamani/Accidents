from django.shortcuts import render
from django.contrib.auth.models import User


def dashboard(request):
    return render(request, "accounts/dashboard.html")
