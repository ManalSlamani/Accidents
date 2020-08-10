from django import forms

class kdeform(forms.Form):
    myRadius= forms.DecimalField(label='Rayon de recherche',  widget=forms.NumberInput(attrs={'min': '0', 'step': '1'}))
    myOpacity= forms.DecimalField(label='Seuil de densité ', widget= forms.NumberInput(attrs={'min': '0', 'step': '0.01'}))

class clusteringform(forms.Form):
    # silhouette = forms.DecimalField(label='Coefficient de Silhouette', disabled=True, widget=forms.NumberInput)
    # inxch = forms.DecimalField(label='Indice CH', disabled=True)
    myEpsilon = forms.DecimalField(label='Epsilon', min_value=0, widget=forms.NumberInput(attrs={'min': '0', 'step': '0.01'}))
    myMinPts = forms.DecimalField(label='minPts ', min_value=0, widget=forms.NumberInput(attrs={'min': '0', 'step': '1'}))



