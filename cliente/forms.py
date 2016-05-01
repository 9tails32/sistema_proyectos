from django import forms


class ClienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre', required=True)
    direccion = forms.CharField(max_length=100, label='Direccion', required=True)
    email = forms.EmailField(label='Email',required=True)

