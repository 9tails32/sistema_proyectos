from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Permission
from .models import Equipo
from proyecto.models import Proyecto
from login.models import Usuario
from django.db.models import Q

# Create the form class.
class EquipoForm(forms.Form):
    nombre = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control',}))
    usuarios = forms.ModelMultipleChoiceField(queryset=Usuario.objects.filter(is_active=True),widget=forms.SelectMultiple(attrs={'class':'form-control',}))
    permisos = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(Q(content_type__app_label='proyecto') |Q(content_type__app_label='equipo') ) ,widget=forms.SelectMultiple(attrs={'class':'form-control',}))
