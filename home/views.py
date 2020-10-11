import datetime
import branca
from django.shortcuts import render,redirect,get_object_or_404
import json
from django.db.models import Count, Q, Sum, Window, F
import datetime as dt # we will need this to convert the date to a number of days since some point
from .models import Accident, NegativeSamples
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
# from .form import CreateUserForm, EditUserForm, intervalledate2
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from tablib import Dataset
from datatableview import Datatable
from .decorators import unauthenticated_user,allowed_users
from sklearn.impute import SimpleImputer
# Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
import numpy as np
import sklearn
from joblib import load, dump
#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import  preprocessing # used for label encoding and imputing NaNs

#------- Variables globales --------#
fullscreen = plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen', force_separate_button=False)
tilesServer="http://192.168.1.5:90/tile/{z}/{x}/{y}.png"

def prepareData(data):
    if 'date' in data.columns:
        # Convert the date into a number (of days since some point)
        fromDate = min(data['date'])
        data['timedelta'] = (data['date'] - fromDate).dt.days.astype(int)
        # print(data[['date', 'timedelta']].head())
        data.drop('date', axis=1, inplace=True)
        data.rename(columns={"timedelta": "date"}, inplace=True)
    if 'annee_permis' in data.columns:
        # Convert ANNEE_PERMIS into a number (of days since some point)
        fromDate = min(data['annee_permis'])
        data['timedelta2'] = (data['annee_permis'] - fromDate).dt.days.astype(int)
        # print(data[['ANNEE_PERMIS', 'timedelta2']].head())
        data.drop('annee_permis', axis=1, inplace=True)
        data.rename(columns={"timedelta2": "annee_permis"}, inplace=True)
    if 'date_naiss_chauff' in data.columns:
        # Convert date_naiss_chauff into a number (of days since some point)
        fromDate = min(data['date_naiss_chauff'])
        data['timedelta3'] = (data['date_naiss_chauff'] - fromDate).dt.days.astype(int)
        # print(data[['date_naiss_chau', 'timedelta3']].head())
        data.drop('date_naiss_chauff', axis=1, inplace=True)
        data.rename(columns={"timedelta3": "date_naiss_chauff"}, inplace=True)
    if 'heure' in data.columns:
        # data.info()
        # Convert the hour into a number (minutes)
        data['Heure'] = pd.to_timedelta((data['heure']).astype(str)).astype('timedelta64[m]').astype(int)
        # print(data[['heure']].tail())
        data.drop('heure', axis=1, inplace=True)
        data.rename(columns={'Heure': 'heure'}, inplace=True)
    if data.isnull().values.any():
        # Create a list of columns that have missing values and an index (True / False)
        df_missing = data.isnull().sum(axis=0).reset_index()
        df_missing.columns = ['column_name', 'missing_count']
        idx_ = df_missing['missing_count'] > 0
        df_missing = df_missing.loc[idx_]
        cols_missing = df_missing.column_name.values
        idx_cols_missing = data.columns.isin(cols_missing)

        # Instantiate an imputer
        imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

        # Fit the imputer using all of our data (but not any dates)
        imputer.fit(data.loc[:, idx_cols_missing])

        # Apply the imputer
        data.loc[:, idx_cols_missing] = imputer.transform(data.loc[:, idx_cols_missing])
    # encoding categorical features: we assign a num value to each categorical feature
    # if ('wilaya' or 'cause_acc' or 'cat_veh' or 'type_route' or 'jour' or 'mois') in attributs:
    for c in data.columns:
        if data[c].dtype == 'object':
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(data[c].values))
            data[c] = lbl.transform(list(data[c].values))
    return (data)

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
        myfilter = intervalledate(request.POST, prefix='charts')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        data = Accident.objects.filter(date__range=[debut, fin])
        evolution = 5
    else:
        data= Accident.objects.all()
        myfilter =  intervalledate(prefix='charts')

    latitude = list(data.values_list("latitude", flat=True))
    #flat to resturn a QuerySet of single values instead of 1-tuples: <QuerySet [1, 2]> instead of <QuerySet [(1,), (2,)]>
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
    myfilter = intervalledate2(prefix='pred')
    clf = load('.\static\\rf_classifier.joblib')
    # mars = pd.read_excel(".\static\\rf_pred.xlsx")
    # predictions = len(mars)
    marsData= Accident.objects.filter(date__year=2014, date__month=3, date__day=31)
    # print(marsData.values('wilaya'))
    marsData= marsData.values('longitude', 'latitude', 'age_chauff', 'annee_permis', 'heure', 'cause_acc', 'date_naiss_chauff', 'date', 'wilaya')

    marsDataCopy= pd.DataFrame(marsData)
    marsData= prepareData(pd.DataFrame(marsData).loc[:, pd.DataFrame(marsData).columns != 'wilaya'])
    predMars= clf.predict(marsData)
    proba = pd.DataFrame(clf.predict_proba(marsData)).rename(columns={0: "proba_0", 1: "proba_1"}, errors="raise")
    pred = pd.DataFrame(clf.predict(marsData)).rename(columns={0: "pred"}, errors="raise")
    result = proba.merge(pred, left_index=True, right_on=None, right_index=True)
    res = pd.concat([marsDataCopy, result], axis=1, join='inner')

    predictions = len(res)

    f = folium.Figure(height=500)
    m = folium.Map(location=[28.5, 2], zoom_start=5, tiles=tilesServer, attr="openmaptiles-server")
    m.add_child(fullscreen)
    colors_array = cm.rainbow(np.linspace(0, 1, predictions))
    rainbow = [colors.rgb2hex(i) for i in colors_array]
    for row in range(len(res)):
        folium.CircleMarker([float(res.iloc[row]['latitude']), float(res.iloc[row]['longitude'])],
                            color=(rainbow[row - 1]), radius=7, fill=True, id=rainbow[row - 1],
                            popup=('Proba:', res.iloc[row]['proba_1'])).add_to(m)
    m.add_to(f)
    m = f._repr_html_()  # updated
    # mars = list(mars)
    total = predictions

    # if request.method == 'POST' and 'predictors' in request.POST:
    #     m=0
    if request.method == 'POST' and 'train' in request.POST:
        intervallePred = intervalledate()
        myfilter = intervalledate2(request.POST, prefix='pred')
        attributs = request.POST.getlist('attributs')
        attributs.append('accident')
        debut = request.POST.get('pred-debutPred')
        fin = request.POST.get('pred-finPred')
        data = Accident.objects.filter(date__range=[debut, fin])
        data1 = NegativeSamples.objects.filter(date__range=[debut, fin])
        data= data.values(*attributs)
        data1 = data1.values(*attributs)
        data= pd.DataFrame(list(data)+list(data1))
        #préparer les données pour le modèle (pas de date, chaine de caractères). La fonction est définie plus haut :)
        prepareData(data)

        #mélanger le dataset
        data = sklearn.utils.shuffle(data)
        X= data[attributs[:-1]]
        # print(X)
        y= data[['accident']]
        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)  # 70% training and 30% test

        # Create a RandomForest Classifier
        clf = RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 512, criterion='gini',  min_samples_leaf= 1 ,min_samples_split= 2)
        # Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(X_train, y_train.values.ravel())
        y_pred = clf.predict(X_test)
        dump(clf, '.\static\\predictors\\clf_classifier.joblib')

        # Model Accuracy, how often is the classifier correct?
        acc= metrics.accuracy_score(y_pred, y_test)
        precision= metrics.precision_score(y_test, y_pred)
        recall= metrics.recall_score(y_test, y_pred)
        f1score= metrics.f1_score(y_test, y_pred, average='weighted')
        roc= metrics.roc_auc_score(y_test, y_pred)
    else:
        data = Accident.objects.all()
        myfilter = intervalledate2(prefix='pred')
        intervallePred = intervalledate()
        acc = '-'
        precision = '-'
        recall = '-'
        f1score = '-'
        roc = '-'
    if request.method == 'POST' and "savePredictor" in request.POST:
        clf = load('.\static\\predictors\\clf_classifier.joblib')
        dump(clf, '.\static\\clf_classifier.joblib')
    context = {'my_map': m, 'predictions':predictions, 'mars':res, 'total':total,
               'myfilter':myfilter, 'acc':acc, 'precision': precision, 'recall': recall,
               'f1score':f1score, 'roc':roc,'intervallePred': intervallePred,}
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

