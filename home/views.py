from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q, Sum, Window
from .models import Sheet1
import folium
from folium import plugins
from django.views.generic import TemplateView


# Create your views here.
def home(request):
    return render(request, 'home/welcome.html')


def get_data(request, *args, **kwargs):
    data = Sheet1.objects.all()
    return render(request, 'home/lineChart.htm', {"data": data})


def all_data(request, *args, **kwargs):
    data = Sheet1.objects.all()
    allData = data.values('date', 'wilaya').annotate(acc_Count=Count('id_accident')).order_by('date').order_by('date')
    allData["date"] = allData["date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    jsonData = allData.to_dict(orient='records')
    return JsonResponse('home/lineChart.htm', {"data": jsonData})


# return JsonResponse(data, safe=False)


def json_example(request):
    return render(request, 'json_example.html')


def chart_data(request):
    dataset = Sheet1.objects \
        .values('nbre_bless') \
        .annotate(total=Count('nbre_bless')) \
        .order_by('nbre_bless')

    port_display_name = dict()
    for mois in Sheet1.mois:
        port_display_name[mois[0]] = mois[1]

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'heatmap'},
        'series': [{
            'name': 'heatmap',
            'data': list(map(lambda row: {'mois': port_display_name[row['nbre_bless']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)


def chart_data(request):
    dataset = Sheet1.objects \
        .values('mois') \
        .annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'), accident=Count('nbre_dec'))

    date_display_name = dict()
    for date_tuple in Sheet1.date:
        date_display_name[date_tuple[0]] = date_tuple[1]

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(lambda row: {'name': date_display_name[row['mois']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)


def monthheatmap(request):
    data = Sheet1.objects.values('mois', 'jour').annotate(accident=Count('nbre_bless')).order_by('jour')
    return render(request, 'home/heatmap.htm', {'monthdata': data})


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def daybarchart(request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    f = folium.Figure(width=650, height=500)
    m = folium.Map(location=[28.5, 1.5], zoom_start=5)

    att = zip(latitude, longitude)
    print(att)
    m.add_child(plugins.HeatMap(att, radius=15, min_opacity=0.8))
    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m}

    ddata = Sheet1.objects.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'),
                                                   accident=Count('nbre_dec')).order_by('jour')
    mdata = Sheet1.objects.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'),
                                                   accident=Count('nbre_dec')).order_by('mois')
    return render(request, 'home/lollipop.htm', {'daydata': ddata, 'monthdata': mdata, 'my_map': m})


# ----------------------------------------------------------------------------------------
def makeHeatmap(request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    m = folium.Map([28, 1.5], zoom_start=5)
    test = folium.Html('<b>Hello world</b>', script=True)
    att = zip(latitude, longitude)
    print(att)
    m.add_child(plugins.HeatMap(att, radius=20))
    m = m._repr_html_()  # updated
    context = {'my_map': m}
    return render(request, "home/lollipop.htm", context)
