from django.forms import DateField, ModelForm, HiddenInput
from django.contrib.admin.widgets import AdminDateWidget
from .models import Proyecto
from Notificaciones.views import notificar_mod_proyecto, notificar_creacion_proyecto

class ProyectoForm(ModelForm):
    """
    Clase para crear Proyecto
    """
    def __init__(self, *args, **kwargs):

        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        fechaInicio = DateField(widget=AdminDateWidget)
        fechaFin = DateField(widget=AdminDateWidget)

    class Meta:
        model = Proyecto
        fields = ('nombre','lider_proyecto', 'cliente', 'fecha_inicio', 'fecha_fin', 'descripcion', 'observaciones')

    def clean(self):
        """
        Validacion de fecha, inicio menor a fin
        """
        cleaned_data = super(ProyectoForm, self).clean()
        diccionario_limpio = self.cleaned_data
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio > fecha_fin:
            msg = "La fecha inicio es mayor a fecha fin"
            self.add_error('fecha_inicio', msg)
            # raise forms.ValidationError("La fecha de inicio es mayor a la de fin")

            # return fecha_inicio

