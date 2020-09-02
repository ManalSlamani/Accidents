from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class kdeform(forms.Form):
    myRadius= forms.DecimalField(label='Rayon de recherche',  widget=forms.NumberInput(attrs={'min': '0', 'step': '1'}))
    myOpacity= forms.DecimalField(label='Seuil de densité ', widget= forms.NumberInput(attrs={'min': '0', 'step': '0.1'}))
class clusteringform(forms.Form):
    # silhouette = forms.DecimalField(label='Coefficient de Silhouette', disabled=True, widget=forms.NumberInput)
    # inxch = forms.DecimalField(label='Indice CH', disabled=True)
    myEpsilon = forms.DecimalField(label='Epsilon', min_value=0, widget=forms.NumberInput(attrs={'min': '0', 'step': '0.01'}))
    myMinPts = forms.DecimalField(label='minPts ', min_value=0, widget=forms.NumberInput(attrs={'min': '0', 'step': '1'}))
class wilaya(forms.Form):
    options=[
        ('--','--'),('adrar','adrar'), ('ain defla','ain defla'), ('ain temouchent','ain temouchent'), ('alger','alger'), ('annaba','annaba'),
        ('bachar','bachar'), ('batna','batna'), ('bejaia','bejaia'), ('biskra','biskra'), ('blida','blida'),
        ('bouira','bouira'), ('boumerdes','boumerdes'), ('chlef','chlef'),
        ('constantine','constantine'), ('djelfa','djelfa'), ('el bayadh','el bayadh'), ('el oued','el oued'), ('el tarf','el tarf'),
        ('ghardaia','ghardaia'), ('guelma','guelma'), ('illizi','illizi'), ('jijel','jijel'), ('khenchela','khenchela'), ('laghouat','laghouat'),
        ('mascara','mascara'), ('medea','medea'), ('mila','mila'), ('mostaganem','mostaganem'), ('msila','msila'), ('naama','naama'), ('oran','oran'),
        ('ouargla','ouargla'), ('oum el bouaghi','oum el bouaghi'), ('relizane','relizane'), ('saida','saida'), ('setif','setif'),
        ('sidi bel abbes','sidi bel abbes'), ('skikda','skikda'), ('souk ahras','souk ahras'), ('tamanrasset','tamanrasset'), ('tebessa','tebessa'),
        ('tiaret','tiaret'), ('.','tindouf'), ('tipaza','tipaza'), ('tissemsilt','tissemsilt'), ('tizi ouzou','tizi ouzou'),
        ('tlemcen','tlemcen'),
    ]
    wilaya=  forms.CharField( widget=forms.Select(choices=options, attrs={'empty_value':"Toutes les wilayas", 'width':'200', 'id':'mywilaya'} ), initial= "--")
class makefilter(forms.Form):
    causes=[('--','--'),]
    routes=[('--','--'),]

    cause= forms.CharField(label='Cause', required=False, widget=forms.Select(choices=causes))
    route= forms.CharField(label= 'Type de route', required=False, widget=forms.Select(choices=routes))
class authentif(forms.Form):
    comptes=[
        ('--','--'),
        ("décideur","Compte décideur"),
        ("admin","Compte admin")
    ]
    user= forms.CharField(label="Nom d'utilisateur", required=True)
    pwd =forms.CharField(label="Mot de passe", required=True)
    compte =forms.CharField(label='Type de compte', required=True, widget=forms.Select(choices=comptes))



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']