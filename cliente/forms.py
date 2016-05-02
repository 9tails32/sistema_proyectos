from django import forms


class ClienteForm(forms.Form):
    """
    Form para editar o crear cliente.
    """
    nombre = forms.CharField(max_length=100, label='Nombre', required=True)
    direccion = forms.CharField(max_length=100, label='Direccion', required=True)
    email = forms.EmailField(label='Email',required=True)

