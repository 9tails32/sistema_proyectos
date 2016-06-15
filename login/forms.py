#encoding:utf-8
from django import forms

class ConfiguracionForm(forms.Form):
    """
    Clases para crear las configuraciones
    """
    """hora_notificaciones = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control time-picker'}),required=True)
    formato = (
        ('htm', 'HTML'),
        ('txt', 'Texto Plano')
    )
    formato_notificaciones = forms.ChoiceField(choices=formato,widget=forms.Select(attrs={'class':'form-control'}),help_text='Formato')
    """
    email_noti = forms.EmailField(required=True)
    noti_creacion_proyecto = forms.BooleanField(widget=forms.CheckboxInput(),
                                                help_text="Notificacion de proyectos creados.",required=False)

    noti_creacion_equipo = forms.BooleanField(widget=forms.CheckboxInput(),
                                              help_text="Notificacion de equipos creados.",required=False)
    noti_cambio_estado_actividades = forms.BooleanField(widget=forms.CheckboxInput(),
                                                help_text="Notificacion de cambio de estado de actividades.",
                                                required=False)
    noti_us_asignado = forms.BooleanField(widget=forms.CheckboxInput(),
                                               help_text="Notificacion de asignacion a un US.", required=False)
    noti_cambio_actividades = forms.BooleanField(widget=forms.CheckboxInput(),
                                                 help_text="Notificacion de cambio de actividades.",
                                              required=False)


