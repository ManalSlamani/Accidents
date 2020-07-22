from django.shortcuts import render
from .models import Sheet1

# Create your views here.
def home(requests):
    return render(requests, 'home/welcome.html')