from django import forms

class kdeform(forms.Form):
    myRadius= forms.DecimalField(label='Rayon de recherche', min_value=0)
    myOpacity= forms.DecimalField(label='Seuil de densité ', min_value=0)
