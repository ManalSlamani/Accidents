from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q
"""from .models import Sheet1"""


# Create your views here.
def home(request):
    return render(request, 'home/welcome.html')


def get_data(request, *args, **kwargs):
    # data = Sheet1.objects.values('wilaya').annotate(total=Count('wilaya')).order_by('wilaya')

    dataa = Sheet1.objects.all()
    return render(request, 'home/lineChart.htm', {'dataa': dataa})

<<<<<<< HEAD
"""def lineChartData(request):
    dataset = Sheet1.objects.values('wilaya').annotate(total=Count('wilaya')).orrder_by('wilaya')
    wilaya_display_name = dict()
    for wilaya_tuple in Sheet1.wilaya:
        wilaya_display_name[wilaya_tuple[0]] = wilaya_tuple[1]
    chart = {
        'chart': {'type': 'line'},
        'title': {'text': 'Accidents'},
        'series': [{
            'name': 'Wilaya d\'accident',
            'data': list(map(lambda row: {'name': wilaya_display_name[row['wilaya']], 'y': row['total']}, dataset))
        }]
    }
    return JsonResponse(chart)"""
=======
    #return JsonResponse(data, safe=False)
>>>>>>> 678fa17b156d2abb55bc202efcccd12bfdda8b28
