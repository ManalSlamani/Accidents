from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q
"""from .models import Sheet1"""


# Create your views here.
def home(requests):
    return render(requests, 'home/welcome.html')


def json_fun(request):
    return render(request, "json_fun.html")


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
