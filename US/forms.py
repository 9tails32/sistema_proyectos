from django import forms
from login.models import Usuario

class TipoUSForm(forms.Form):
    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control'}))

class ActividadesForm(forms.Form):
    nombre = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control'}))

class USForm(forms.Form):
    descripcion_corta = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',}), max_length=140, help_text='Introduzca una breve descripcion del proyecto')
    descripcion_larga = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',}), max_length=420, help_text='Introduzca una descripcion del proyecto')
    tiempo_planificado = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',}))
    valor_negocio = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',}),min_value=1,max_value=5)  # 1 a 5
    urgencia = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',}),min_value=1,max_value=5) # 1 a 5
    usuario_asignado = forms.ModelChoiceField(queryset=Usuario.objects.none(),widget=forms.Select(attrs={'class':'form-control',}),required=False)
