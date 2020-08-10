from django.http import JsonResponse
from django.shortcuts import render
import json
from django.db.models import Count, Q, Sum, Window, F
from .models import Sheet1
import folium
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import pandas as pd
from .form import kdeform
from joblib import dump, load


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


    wdata= Sheet1.objects.values("wilaya").annotate(accidents=Sum('accident'), dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')).order_by('wilaya')
    ddata =Sheet1.objects.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'), accidents=Sum('accident')).order_by('-accidents')
    accident =Sheet1.objects.values("mois").annotate(accidents=Sum('accident'), dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'))
    mdata = (Sheet1.objects.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')))
    routedata = Sheet1.objects.values('type_route').annotate(route_count=Count('type_route')*100/acc)
    catdata = Sheet1.objects.values('cat_veh').annotate(cat_count=Count('cat_veh'))
    hdata= list(Sheet1.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure').order_by('-accidents'))[:7]
    # hdata= list(Sheet1.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure'))
    temperaturedata= Sheet1.objects.values("age_chauff").annotate(accidents=Sum('accident')).order_by('age_chauff')
    precipitationdata= Sheet1.objects.values("couverturenuage").annotate(accidents=Sum('accident')).order_by('couverturenuage')



    cum_acc = Sheet1.objects.values('mois').annotate(cum_acc=Window(Count('mois'), order_by=F('mois').asc())).distinct()
    evolution = round(
    ((list(accident.distinct())[-1]['accidents'] - list(accident.distinct())[-2]['accidents']) * 100 / acc), 2)



    causes= list(Sheet1.objects.values("cause_acc").annotate(cause=Count("cause_acc")).order_by('-cause'))
    causes= causes[:6]


    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata,'accidents': acc,
                                                  "bless":bless, "dec":dec, "evolution":evolution, 'causes':causes, 'accident':accident,
                                                  'cum_acc':cum_acc, 'hourdata':hdata, 'temperaturedata':temperaturedata,
                                                  "precipitationdata":precipitationdata})


# ----------------------------------------------------------------------------------------
def makeHeatmap(request, myRadius=15, myOpacity=0.8):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    # f = folium.Figure(width=650, height=500, title="Heatmap")
    f = folium.Figure()
    m = folium.Map(location=[28.5, 1.5], zoom_start=5)
    att = zip(latitude, longitude)
    if request.method == 'POST':
        form = kdeform(request.POST)
    else:
        form = kdeform()
    myRadius = request.POST.get('myRadius')
    print((myRadius))
    myOpacity = request.POST.get('myOpacity')
    print(type(myOpacity))
    if (myRadius == None):
       m.add_child(plugins.HeatMap(att, radius=15, min_opacity=0.8))
    else:
        # m.add_child(plugins.HeatMap(att, radius=myRadius, min_opacity=myOpacity))
        print(type(myOpacity))
        HeatMap(att, radius=float(myRadius), min_opacity=float(myOpacity)).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        folium.LayerControl().add_to(m)

        # m.add_child(plugins.HeatMap(att, radius=myRadius, min_opacity=myOpacity))
    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m, 'form':form}
    return render(request, "home/heatmap.htm", context)

# ----------------------------------------------------------------------------------------

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
from collections import Counter
def makeClusters(request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    att= list(zip(latitude,longitude))
    dbscan_data_scaler = StandardScaler().fit(att)
    dbscan_data = dbscan_data_scaler.transform(att)
    model = DBSCAN(eps=0.02, min_samples=4).fit(dbscan_data)
    model
    clus_number = len(set(model.labels_)) - (-1 if -1 in model.labels_ else 0)
    # print(set(model.labels_))
    # print(clus_number)
    outliers_df = pd.DataFrame(att)[model.labels_ == -1]
    clusters_df = pd.DataFrame(att)[model.labels_ != -1]
    model.labels_
    colors = model.labels_
    pd.DataFrame(colors).head()
    colors_clusters = colors[colors != -1]
    colors_outliers = "black"
    clusters = Counter(model.labels_)
    print(clusters)

    df = pd.DataFrame(Sheet1.objects.all())
    # f = folium.Figure(width=650, height=500, title="Heatmap")
    f = folium.Figure()
    m = folium.Map(location=[28.5, 1.5], zoom_start=5)
    # for row in clusters_df:
    #     folium.Marker(location=[row[0],row[1]]).add_to(m)$
    import matplotlib.cm as cm
    import matplotlib.colors as colors
    import  random
    colors_array = cm.rainbow(np.linspace(0, 1, len(clusters)))
    rainbow = [colors.rgb2hex(i) for i in colors_array]
    markers_colors = []
    for lat, long in att:
        folium.vector_layers.CircleMarker(
            [lat, long],
            radius=6, fill=True,  fill_opacity=0.9, color=rainbow[random.randint(2,148)-1]).add_to(m)
    att = list(zip(latitude, longitude))

    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m}
    return render(request,'home/clustering.html', context)

# ----------------------------------------------------------------------------------------
def makePrediction (request):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))

    f = folium.Figure( height=500)
    # f = folium.Figure()
    m = folium.Map(location=[28.5, 1.5], zoom_start=4.5)

    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m}
    return render(request, 'home/prediction.html', context)