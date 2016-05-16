from proyecto.models import  Proyecto
from django import forms
from django.db.models import Q
from US.models import US

class AsignarUSForm(forms.Form):
    uss = forms.ModelMultipleChoiceField(queryset=US.objects.none(),widget=forms.SelectMultiple(attrs={'class':'form-control',}))

class SprintForm(forms.Form):

    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control',}))

