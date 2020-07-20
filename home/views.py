from django.shortcuts import render
from Accidents.models import Sheet1

# Create your views here.
def home(requests):
    return render(requests,'home/welcome.html')