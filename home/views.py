from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q, Sum, Window, F
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

    bless = (Sheet1.objects.values("accident").annotate(accidents=Sum('nbre_bless'))[0]['accidents'])
    dec = (Sheet1.objects.values("accident").annotate(accidents=Sum('nbre_dec'))[0]['accidents'])
    acc = (Sheet1.objects.values("accident").annotate(accidents=Count('accident'))[0]['accidents'])


    wdata= Sheet1.objects.values("wilaya").annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')).order_by('wilaya')
    ddata =Sheet1.objects.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'), accidents=Sum('accident'))
    accident =Sheet1.objects.values("mois").annotate(accidents=Sum('accident'), dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'))
    mdata = (Sheet1.objects.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')))
    routedata = Sheet1.objects.values('type_route').annotate(route_count=Count('type_route')*100/acc)
    catdata = Sheet1.objects.values('cat_veh').annotate(cat_count=Count('cat_veh'))
    hdata= list(Sheet1.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure').order_by('-accidents'))[:7]
    # hdata= list(Sheet1.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure'))

    print(hdata)
    cum_acc = Sheet1.objects.values('mois').annotate(cum_acc=Window(Count('mois'), order_by=F('mois').asc())).distinct()
    evolution = round(
    ((list(accident.distinct())[-1]['accidents'] - list(accident.distinct())[-2]['accidents']) * 100 / acc), 2)



    causes= list(Sheet1.objects.values("cause_acc").annotate(cause=Count("cause_acc")).order_by('-cause'))
    causes= causes[:6]


    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata,'accidents': acc,
                                                  "bless":bless, "dec":dec, "evolution":evolution, 'causes':causes, 'accident':accident,
                                                  'cum_acc':cum_acc, 'hourdata':hdata})


# ----------------------------------------------------------------------------------------
def makeHeatmap(request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    # f = folium.Figure(width=650, height=500, title="Heatmap")
    f = folium.Figure()
    m = folium.Map(location=[28.5, 1.5], zoom_start=5)

    att = zip(latitude, longitude)
    print(att)
    m.add_child(plugins.HeatMap(att, radius=15, min_opacity=0.8))
    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m}
    return render(request, "home/heatmap.htm", context)

# ----------------------------------------------------------------------------------------
def makeClusters(request):
    return (request)