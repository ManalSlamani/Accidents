from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q
from .models import Sheet1


# Create your views here.
def home(request):
    return render(request, 'home/welcome.html')


def get_data(request, *args, **kwargs):
    # data = Sheet1.objects.values('wilaya').annotate(total=Count('wilaya')).order_by('wilaya')

    dataa = Sheet1.objects.all()
    return render(request, 'home/lineChart.htm', {'dataa': dataa})

    #return JsonResponse(data, safe=False)
