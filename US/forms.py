from django import forms

class TipoUSForm(forms.Form):
    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control'}))

class ActividadesForm(forms.Form):
    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control'}))
