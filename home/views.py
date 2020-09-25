import datetime
import branca
from django.shortcuts import render,redirect,get_object_or_404
import json
from django.db.models import Count, Q, Sum, Window, F
from .models import Accident
from django.http import JsonResponse
from django.core import serializers
from import_export import resources
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
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
from .form import CreateUserForm, EditUserForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from tablib import Dataset
from datatableview import Datatable
from .decorators import unauthenticated_user,allowed_users
#------- Variables globales --------#
fullscreen = plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen', force_separate_button=False)
tilesServer="http://192.168.1.5:90/tile/{z}/{x}/{y}.png"


# class AccidentDatatableView(DatatablesServerSideView):
# 	# We'll use this model as a data source.
# 	model = Accident
#
# 	# Columns used in the DataTables
# 	columns = ['name', 'age', 'manager', 'department']
#
# 	# Columns in which searching is allowed
# 	searchable_columns = ['name', 'manager', 'department']
#
# 	# Replacement values for foreign key fields.
# 	# Here, the "manager" field points toward another employee.
# 	foreign_fields = {'manager': 'manager__name'}
#
# 	# By default, the entire collection of objects is accessible from this view.
# 	# You can change this behaviour by overloading the get_initial_queryset method:
# 	def get_initial_queryset(self):
# 		qs = super(PeopleDatatableView, self).get_initial_queryset()
# 		return qs.filter(manager__isnull=False)
#
# 	# You can also add data within each row using this method:
# 	def customize_row(self, row, obj):
# 		# 'row' is a dictionnary representing the current row, and 'obj' is the current object.
# 		row['age_is_even'] = obj.age%2==0


@login_required(login_url='authentif')
def home(request):
    return render(request, 'home/welcome.html')

@login_required(login_url='authentif')
def get_data(request, *args, **kwargs):
    data = Accident.objects.all()
    return render(request, 'home/lineChart.htm', {"data": data})


# ------------------------------------------------------------------------------
@login_required(login_url='authentif')
def daybarchart(request):
    f = folium.Figure()
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
    m.add_child(fullscreen)
    if request.method == 'POST':
        myfilter = intervalledate(request.POST)
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        data = Accident.objects.filter(date__range=[debut, fin])
        evolution = 5
    else:
        data= Accident.objects.all()
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
    # hdata= list(Accident.objects.values('heure').annotate(accidents=Count('accident')).order_by('heure'))
    temperaturedata = data.values("age_chauff").annotate(accidents=Sum('accident')).order_by('age_chauff')
    precipitationdata = data.values("couverturenuage").annotate(accidents=Sum('accident')).order_by(
        'couverturenuage')

    cum_acc = data.values('mois').annotate(cum_acc=Window(Count('mois'), order_by=F('mois').asc())).distinct()

    causes = list(data.values("cause_acc").annotate(cause=Count("cause_acc")).order_by('-cause'))
    causes = causes[:6]
    att = list(zip(latitude, longitude))
    MarkerCluster(att, options={'maxClusterRadius':50}).add_to((folium.FeatureGroup(name='Regroupement').add_to(m)))
    HeatMap(att, radius=15, min_opacity=0.8).add_to(folium.FeatureGroup(name='HeatMap').add_to(m))
    colormap = branca.colormap.LinearColormap(colors=['blue', 'lime', 'yellow', 'red'], vmin=0, vmax=0.8)
    colormap.add_to(m)  # add color bar at the top of the map
    # folium.LayerControl().add_to(m)
    folium.map.LayerControl('topleft', collapsed=True).add_to(m)
    vmax= len(att)/2
    m.add_to(f)
    m = f._repr_html_()  # updated


    return render(request, 'home/myCharts.html', {'daydata': ddata, 'monthdata': mdata, 'my_map': m, 'wilaya_data': wdata, 'routedata': routedata, 'catdata': catdata,'accidents': acc,
                                                  "bless":bless, "dec":dec, "evolution":evolution, 'causes':causes, 'accident':accident,
                                                  'cum_acc':cum_acc, 'hourdata':hdata, 'temperaturedata':temperaturedata,
                                                  "precipitationdata":precipitationdata, 'myfilter':myfilter})

# ----------------------------------------------------------------------------------------
@login_required(login_url='authentif')
def makeHeatmap(request, myRadius=15, myOpacity=0.8):
    latitude = list(Accident.objects.values_list("latitude", flat=True))
    longitude = list(Accident.objects.values_list("longitude", flat=True))
    f = folium.Figure()
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
    m.add_child(fullscreen)
    att = zip(latitude, longitude)
    if request.method == 'POST':
        form = kdeform(request.POST)
    else:
        form = kdeform()
    myRadius = request.POST.get('myRadius')
    # print((myRadius))
    myOpacity = request.POST.get('myOpacity')
    # print(type(myOpacity))
    if (myRadius == None):
        colormap = branca.colormap.LinearColormap(colors=['blue','lime','yellow', 'red'],  vmin=0, vmax=0.8)
        colormap.add_to(m)  # add color bar at the top of the map
        m.add_child(plugins.HeatMap(att, radius=15, min_opacity=0.8))

    else:
        colormap = branca.colormap.LinearColormap(colors=['blue','lime','yellow', 'red'],  vmin=0, vmax=float(myOpacity))
        colormap.add_to(m)  # add color bar at the top of the map
        HeatMap(att, radius=float(myRadius), min_opacity=float(myOpacity)).add_to(folium.FeatureGroup(name='HeatMap').add_to(m))
        folium.LayerControl().add_to(m)


        # m.add_child(plugins.HeatMap(att, radius=myRadius, min_opacity=myOpacity))
    m.add_to(f)
    m = f._repr_html_()  # updated
    context = {'my_map': m, 'form':form}
    return render(request, "home/heatmap.htm", context)

# ----------------------------------------------------------------------------------------
@login_required(login_url='authentif')
def makeClusters(request):

    df=pd.DataFrame(Accident.objects.values('latitude','longitude','cause_acc','temperature','precipitation','nbre_bless', 'nbre_dec','age_chauff'))
    fig = folium.Figure()
    # m = folium.Map(location=[28.5, 1.5], zoom_start=5)
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
    m.add_child(fullscreen)
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
        m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
        m.add_child(fullscreen)
        colors_array = cm.rainbow(np.linspace(0, 1, len(clusters)))
        rainbow = [colors.rgb2hex(i) for i in colors_array]
        for row in range(len(clusters_df)):
            folium.vector_layers.CircleMarker(
                [float(clusters_df.iloc[row]['latitude']), float(clusters_df.iloc[row]['longitude'])],
                radius=5, fill=True, popup= ('Cause:', clusters_df.iloc[row]['cause_acc'], 'NBRE_Bless:', clusters_df.iloc[row]['nbre_bless']),
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
                radius=8, fill=True, popup=('Cause:', clusters_df.iloc[row]['cause_acc'], 'Nbre_bless',clusters_df.iloc[row]['nbre_bless']),
                fill_opacity=1, color=random.choice(rainbow)).add_to(m)

    m.add_to(fig)
    m = fig._repr_html_()  # updated
    context = {'my_map': m, 'formClus':formClus, 'silhouette':silhouette, 'inxch':inxch, 'nbr_clusters':nbr_clusters,
               'outliers':outliers}
    return render(request,'home/clustering.html', context)

# ----------------------------------------------------------------------------------------
@login_required(login_url='authentif')
def makePrediction (request):
    mars= pd.read_excel(".\static\\rf_pred.xlsx")
    predections=len(mars)
    f = folium.Figure( height=500)
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
    m.add_child(fullscreen)
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




@unauthenticated_user
def authentification (request):
    form = authentif()

    if request.method == 'POST':
        form = authentif(request.POST)
        if form.is_valid():
            # username = request.GET('userName')

            username = form.cleaned_data.get('user')
            print(username)
            # password = request.GET('pwd')

            password = form.cleaned_data.get('pwd')
            user = authenticate(request,username = username,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Nom Utilisateur ou mot de passe incorrect')
                return render(request, 'home/authentification.html', {'username': username, 'pwd':password})

    return render(request, 'home/authentification.html', {'form':form} )




def logoutUser(request):
    logout(request)
    return redirect('authentif')



@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':

            # form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Compte créé pour ' + user)
            return redirect('authentif')

    return render(request,'home/register.html',{"form":form})

@login_required(login_url='authentif')
def EditProfilePage(request):
    form = EditUserForm()

    if request.method == 'POST':

            # form = UserCreationForm(request.POST)
        form = EditUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Compte modifié pour ' + user)
            return redirect('home')

    return render(request,'home/edit_profile.html',{"form":form})





class ShowProfileView(DetailView):
    model = User
    template_name = 'home/profile.html'

    def get_context_data(self,*args,**kwargs):
        users = User.objects.all()
        context = super(ShowProfileView,self).get_context_data(*args,**kwargs)
        page_user = get_object_or_404(User,id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class UserEditView(generic.UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'home/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


@login_required(login_url='authentif')
def allData(request):
    # context = {}
    data= Accident.objects.all()
    # data = json.dumps(data, cls=DjangoJSONEncoder)
    # data=serializers.serialize('json', data)
    # context['data']= data
    total = len(data)
    wilayaform = wilaya()
    # form = uploadFiles()
    context= {'data':data, 'wilayaform':wilayaform, 'total':total,}
    return render(request,'home/bdd.html', context)
    # return JsonResponse(data, safe=False)

# @login_required(login_url='authentif')
# def allData(request):
#     context = {}
#     data= Accident.objects.all()
#     total = len(data)
#     wilayaform = wilaya()
#     # form = uploadFiles()
#     context= {'data':data, 'wilayaform':wilayaform, 'total':total,}
#     return render(request,'home/bdd.html', context)

@login_required(login_url='authentif')
def uploadData(request):
    if request.method == 'POST':
        # data_resource = AccidentResource()
        data_resource= resources.modelresource_factory(model=models.Accident)()
        dataset = Dataset()
        new_data = request.FILES['importData']
        imported_data = dataset.load(new_data.read().decode('utf-8'),format='csv')
        result = data_resource.import_data(dataset, dry_run=True)  # Testing data import
        if not result.has_errors():
            data_resource.import_data(dataset, dry_run=False)  # Actually import now
    wilayaform = wilaya()
    data = Accident.objects.all().values()
    total = len(data)
    context ={'data':data, 'wilayaform':wilayaform, 'total':total,}
    return render(request, 'home/bdd.html', context)
@login_required(login_url='authentif')
def changeWilaya(request):
    wilayaform = wilaya(request.POST)
    mywilaya= request.POST.get('wilaya')
    data = Accident.objects.filter(wilaya=mywilaya)
    total=len(data)
    form = uploadFiles()
    context = {'data':data, 'wilayaform':wilayaform, 'total':total,'form': form }
    return render(request, 'home/bdd.html', context)

@login_required(login_url='authentif')
def help (request):
    return render(request, "home/help.html")

