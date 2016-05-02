from django import forms


class ClienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre', required=True)
    direccion = forms.CharField(max_length=100, label='Direccion', required=True)
    email = forms.EmailField(label='Email',required=True)

class TelefonoForm(forms.Form):
    telefono = forms.IntegerField(min_value=0,required=True, widget=forms.NumberInput(attrs={'class':'form-control',}))

