import datetime
import branca
from django.shortcuts import render
import json
from django.db.models import Count, Q, Sum, Window, F
from .models import Sheet1
import folium
from folium import plugins, Popup
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import pandas as pd
from .form import *
import matplotlib.cm as cm
import matplotlib.colors as colors
import random
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
from collections import Counter, defaultdict
from joblib import  load
from sklearn import metrics
import leaflet


# Create your views here.
def home(request):
    return render(request, 'home/welcome.html')


def get_data(request, *args, **kwargs):
    data = Sheet1.objects.all()
    return render(request, 'home/lineChart.htm', {"data": data})




# ------------------------------------------------------------------------------
def daybarchart(request):
    f = folium.Figure()
    m = folium.Map(location=[28.5, 2], zoom_start=5,
                   tiles="http://192.168.99.100:32768/styles/osm-bright/{z}/{x}/{y}.png",
                   attr="local-map-server")
    if request.method == 'POST':
        myfilter = intervalledate(request.POST)
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        data = Sheet1.objects.filter(date__range=[debut, fin])
        evolution = 5
    else:
        data= Sheet1.objects.all()
        myfilter = intervalledate()

    latitude = list(data.values_list("latitude", flat=True))
    longitude = list(data.values_list("longitude", flat=True))
    bless = (data.values("accident").annotate(accidents=Sum('nbre_bless'))[0]['accidents'])
    dec = (data.values("accident").annotate(accidents=Sum('nbre_dec'))[0]['accidents'])
    acc = (data.values("accident").annotate(accidents=Count('accident'))[0]['accidents'])
    wdata = data.values("wilaya").annotate(accidents=Sum('accident'), dec_count=Sum('nbre_dec'),
                                           bless_count=Sum('nbre_bless')).order_by('wilaya')
    ddata = data.values('jour').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless'),
                                         accidents=Sum('accident')).order_by('-accidents')
    accident = data.values("mois").annotate(accidents=Sum('accident'), dec_count=Sum('nbre_dec'),
                                            bless_count=Sum('nbre_bless'))
    if len(accident)>1:
        evolution = round(
        ((list(accident.distinct())[-1]['accidents'] - list(accident.distinct())[-2]['accidents']) * 100 / acc), 2)
    else:
        evolution=0

    mdata = (data.values('mois').annotate(dec_count=Sum('nbre_dec'), bless_count=Sum('nbre_bless')))
    routedata = data.values('type_route').annotate(route_count=Count('type_route')).order_by(
        '-route_count')[:8]
    catdata = list(data.values('cat_veh').annotate(cat_count=Count('cat_veh')).order_by('-cat_count'))[:8]
    hdata = list(
        data.values('heure').annotate(accidents=Count('accident')).order_by('heure').order_by('heure'))
    # hdata= list(Sheet1.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure'))
    temperaturedata = data.values("age_chauff").annotate(accidents=Sum('accident')).order_by('age_chauff')
    precipitationdata = data.values("couverturenuage").annotate(accidents=Sum('accident')).order_by(
        'couverturenuage')

    cum_acc = data.values('mois').annotate(cum_acc=Window(Count('mois'), order_by=F('mois').asc())).distinct()

    causes = list(data.values("cause_acc").annotate(cause=Count("cause_acc")).order_by('-cause'))
    causes = causes[:6]
    att = list(zip(latitude, longitude))
    MarkerCluster(att).add_to(m)
    vmax= len(att)
    colormap = branca.colormap.LinearColormap(colors=['green', 'yellow', 'brown'], index=[0,300, vmax], vmin=0, vmax=vmax)
    colormap.add_to(m)  # add color bar at the top of the map
    m.add_to(f)
    m = f._repr_html_()  # updated


    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata,'accidents': acc,
                                                  "bless":bless, "dec":dec, "evolution":evolution, 'causes':causes, 'accident':accident,
                                                  'cum_acc':cum_acc, 'hourdata':hdata, 'temperaturedata':temperaturedata,
                                                  "precipitationdata":precipitationdata, 'myfilter':myfilter})

# ----------------------------------------------------------------------------------------
def makeHeatmap(request, myRadius=15, myOpacity=0.8):
    latitude = list(Sheet1.objects.values_list("latitude", flat=True))
    longitude = list(Sheet1.objects.values_list("longitude", flat=True))
    f = folium.Figure()
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles="http://192.168.99.100:32768/styles/osm-bright/{z}/{x}/{y}.png", attr="openmaptiles-server")
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
        colormap = branca.colormap.LinearColormap(colors=['blue','lime','yellow', 'red'],  vmin=0, vmax=0.8)
        colormap.add_to(m)  # add color bar at the top of the map
        m.add_child(plugins.HeatMap(att, radius=15, min_opacity=0.8))
    else:
        colormap = branca.colormap.LinearColormap(colors=['blue','lime','yellow', 'red'],  vmin=0, vmax=float(myOpacity))
        colormap.add_to(m)  # add color bar at the top of the map
        HeatMap(att, radius=float(myRadius), min_opacity=float(myOpacity)).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        folium.LayerControl().add_to(m)

        # m.add_child(plugins.HeatMap(att, radius=myRadius, min_opacity=myOpacity))
    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m, 'form':form}
    return render(request, "home/heatmap.htm", context)

# ----------------------------------------------------------------------------------------
def makeClusters(request):
    df=pd.DataFrame(Sheet1.objects.values('latitude','longitude','cause_acc','temperature','precipitation','nbre_bless', 'nbre_dec','age_chauff'))
    fig = folium.Figure()
    # m = folium.Map(location=[28.5, 1.5], zoom_start=5)
    m = folium.Map(location=[28.5, 2], zoom_start=5,
                   tiles="http://192.168.99.100:32768/styles/osm-bright/{z}/{x}/{y}.png", attr="openmaptiles-server")

    if request.method == 'POST':
        formClus = clusteringform(request.POST)
    else:
        formClus = clusteringform()
    myEpsilon = request.POST.get('myEpsilon')

    myMinPts  = request.POST.get('myMinPts')

    popup =Popup(width=80, show=False)

    if (myEpsilon == None):
        model = load('home/dbscan.joblib')
        silhouette= 0.642
        inxch= 57.086
        nbr_clusters= 263
        outliers= 152

        clusters_df = df[model.labels_ != -1]
        clusters = Counter(model.labels_)
        m = folium.Map(location=[28.5, 2], zoom_start=5,
                       tiles="http://192.168.99.100:32768/styles/osm-bright/{z}/{x}/{y}.png",
                       attr="openmaptiles-server")
        colors_array = cm.rainbow(np.linspace(0, 1, len(clusters)))
        rainbow = [colors.rgb2hex(i) for i in colors_array]
        for row in range(len(clusters_df)):
            folium.vector_layers.CircleMarker(
                [float(clusters_df.iloc[row]['latitude']), float(clusters_df.iloc[row]['longitude'])],
                radius=5, fill=True, popup= ('NBRE_Bless:', clusters_df.iloc[row]['nbre_bless'], 'NBRE_Dec:', clusters_df.iloc[row]['nbre_dec']),
                fill_opacity=1, color=random.choice(rainbow)).add_to(m)
        # m.save('clusters.html')
    else:
        att= df[['longitude','latitude']]
        dbscan_data=pd.DataFrame(att)
        dbscan_data = dbscan_data.values.astype('float32', copy=False)
        dbscan_data_scaler = StandardScaler().fit(dbscan_data)
        dbscan_data = dbscan_data_scaler.transform(dbscan_data)
        model = DBSCAN(eps=float(myEpsilon), min_samples=float(myMinPts)).fit(dbscan_data)
        silhouette= metrics.silhouette_score(dbscan_data, model.labels_)
        inxch= metrics.calinski_harabasz_score(dbscan_data, model.labels_)
        clusters_df = df[model.labels_ != -1]
        a=False
        core = model.core_sample_indices_
        print(len(clusters_df))
        clusters = Counter(model.labels_)
        nbr_clusters= len(set(model.labels_)) - (-1 if -1 in model.labels_ else 0)
        outliers= len(df[model.labels_==-1])
        colors_array = cm.rainbow(np.linspace(0, 1, len(clusters)))
        rainbow = [colors.rgb2hex(i) for i in colors_array]

        for row in range(len(clusters_df)):
            folium.vector_layers.CircleMarker(
                [float(clusters_df.iloc[row]['latitude']), float(clusters_df.iloc[row]['longitude'])],
                radius=8, fill=True, popup=(clusters_df.iloc[row]['cause_acc'], clusters_df.iloc[row]['nbre_bless']),
                fill_opacity=1, color=random.choice(rainbow)).add_to(m)

    m.add_to(fig)
    m = fig._repr_html_()  # updated
    context = {'my_map': m, 'formClus':formClus, 'silhouette':silhouette, 'inxch':inxch, 'nbr_clusters':nbr_clusters,
               'outliers':outliers}
    return render(request,'home/clustering.html', context)

# ----------------------------------------------------------------------------------------
def makePrediction (request):
    mars= pd.read_excel(".\static\\rf_pred.xlsx")
    print(mars.date)
    # mars.date= datetime.date(mars.date)
    predections=len(mars)
    f = folium.Figure( height=500)
    # f = folium.Figure()
    # m = folium.Map(location=[28.5, 1.5], zoom_start=4.5)
    m = folium.Map(location=[28.5, 2], zoom_start=5,
                   tiles="http://192.168.99.100:32768/styles/osm-bright/{z}/{x}/{y}.png", attr="openmaptiles-server")

    colors_array = cm.rainbow(np.linspace(0,1 , len(mars)))
    rainbow = [colors.rgb2hex(i) for i in colors_array]
    for row in range(len(mars)):
        folium.CircleMarker([float(mars.iloc[row]['Latitude']), float(mars.iloc[row]['Longitude'])],
                            color=(rainbow[row-1]), radius=7,fill=True, id= rainbow[row-1],
                            popup=('Prpba:',mars.iloc[row]['proba_1'])).add_to(m)
    m.add_to(f)
    m = f._repr_html_()  # updated
    # mars = list(mars)
    total= len(mars)
    context = {'my_map': m, 'predections':predections, 'mars':mars, 'total':total, 'rainbow':rainbow}
    return render(request, 'home/prediction.html', context)

def allData(request):
    data= Sheet1.objects.all().values()
    if request.method == 'POST':
        wilayaform = wilaya(request.POST)
        mywilaya= request.POST.get('wilaya')
        data = Sheet1.objects.filter(wilaya=mywilaya)
        total=len(data)
    else:
        total= len(data)
        wilayaform = wilaya()

    context= {'data':data, 'form':wilayaform, 'total':total}
    return render(request,'home/bdd.html', context)

def authentification (request):
    if request.method == 'POST':
        form = authentif(request.POST)
    else:
        form = authentif()

    return render(request, 'home/authentification.html', {"form": form} )

def help (request):
    return render(request, "home/help.html")