#encoding:utf-8
from django import forms
from login.models import Usuario
from abm_clientes.models import Cliente
from django.utils import timezone

class ProyectoForm(forms.Form):
    """
    Clase para crear Proyecto
    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('ANU', 'Anulado'),
        ('ACT', 'Activo'),
        ('FIN', 'Finalizado'),)
    nombre = forms.CharField(max_length=50)
    fecha_inicio = forms.DateField(widget=forms.SelectDateWidget)
    fecha_fin = forms.DateField(widget=forms.SelectDateWidget)
    lider_proyecto = forms.ModelChoiceField(queryset=Usuario.objects.all())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    descripcion = forms.CharField(widget=forms.Textarea, max_length=140, help_text='Introduzca una breve reseña del proyecto')
    estado = forms.ChoiceField(choices=opciones_estado, help_text='Estado del proyecto')
    observaciones = forms.CharField(widget=forms.Textarea,max_length=140, initial='No hay observaciones.')


    def clean(self):
        """
        Validacion de fecha, inicio menor a fin
        """
        cleaned_data = super(ProyectoForm, self).clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio > fecha_fin:
            msg = "La fecha inicio es mayor a fecha fin"
            self.add_error('fecha_inicio', msg)
            # raise forms.ValidationError("La fecha de inicio es mayor a la de fin")

            # return fecha_inicio

