from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
def home(requests):
    return render(requests,'home/welcome.html')