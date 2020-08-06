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
    ddata =Sheet1.objects.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'))
    # accident =Sheet1.objects.values("accident").annotate(accidents=Count('accident'))
    acc= (Sheet1.objects.values("accident").annotate(accidents=Count('accident'))[0]['accidents'])
    mdata = (Sheet1.objects.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')))
    bless= (Sheet1.objects.values("accident").annotate(accidents=Sum('nbre_bless'))[0]['accidents'])
    dec= (Sheet1.objects.values("accident").annotate(accidents=Sum('nbre_dec'))[0]['accidents'])
    routedata = Sheet1.objects.values('type_route').annotate(route_count=Count('type_route'))
    catdata = Sheet1.objects.values('cat_veh').annotate(cat_count=Count('cat_veh'))

    causes= list(Sheet1.objects.values("cause_acc").annotate(cause=Count("cause_acc")).order_by('-cause'))
    print(causes[0])
    print(causes[1]["cause"])
    causes= causes[:6]
    print(causes[0])
    # cause_display_name = dict()
    # for port_tuple in Sheet1.cause_acc:
    #      cause_display_name[port_tuple[0]] = port_tuple[1]
    # pie = {
    #     'chart': {'type': 'pie'},
    #     'title': {'text': 'Titanic Survivors by Ticket Class'},
    #     'series': [{
    #         'name': 'Embarkation Port',
    #         'data': list(map(lambda row: {'name': cause_display_name[row['cause_acc']], 'y': row['cause']}, causes))
    #     }]}

    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata,'accidents': acc,
                                                  "bless":bless, "dec":dec, 'causes':causes})


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