from proyecto.models import  Proyecto
from django import forms
from django.db.models import Q

class SprintForm(forms.Form):

    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control',}))

