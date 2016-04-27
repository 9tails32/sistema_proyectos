from django import forms


class ClienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    direccion = forms.CharField(max_length=100, label='Direccion')
    email = forms.EmailField(label='Email')

