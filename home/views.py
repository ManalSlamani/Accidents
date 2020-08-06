from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q, Sum, Window
from .models import Sheet1
import folium
from folium import plugins
from folium.plugins import MarkerCluster
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




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def daybarchart(request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    f = folium.Figure()
    m = folium.Map(location=[28.5, 1.5], zoom_start=5)
    att = list(zip(latitude, longitude))
    MarkerCluster(att).add_to(m)

    m.add_to(f)

    m = f._repr_html_()  # updated
    context = {'my_map': m}
    wdata= Sheet1.objects.values("wilaya").annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')).order_by('wilaya')
    ddata =Sheet1.objects.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'),accident=Count('nbre_dec'))
    mdata = Sheet1.objects.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'),accident=Count('nbre_dec'))
    routedata = Sheet1.objects.values('type_route').annotate(route_count=Count('type_route'))
    catdata = Sheet1.objects.values('cat_veh').annotate(cat_count=Count('cat_veh'))
    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata})


# ----------------------------------------------------------------------------------------
def makeHeatmap(request):
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
    return render(request, "home/heatmap.htm", context)
