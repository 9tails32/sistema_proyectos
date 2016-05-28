#encoding:utf-8
from django import forms

class ConfiguracionForm(forms.Form):
    """
    Clases para crear las configuraciones
    """
    hora_notificaciones = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control time-picker'}),required=True)
    formato = (
        ('htm', 'HTML'),
        ('txt', 'Texto Plano')
    )
    formato_notificaciones = forms.ChoiceField(choices=formato,widget=forms.Select(attrs={'class':'form-control'}),help_text='Formato')
    noti_creacion_proyecto = forms.BooleanField(widget=forms.CheckboxInput(),help_text="Notificacion de proyectos creados",required=False)
    noti_creacion_usuario = forms.BooleanField(widget=forms.CheckboxInput(),help_text="Notificacion de usuarios creados",required=False)
    noti_creacion_equipo = forms.BooleanField(widget=forms.CheckboxInput(),help_text="Notificacion de equipos creados",required=False)


