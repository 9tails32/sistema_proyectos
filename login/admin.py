from django.contrib import admin
from .models import Usuario

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('cedula','direccion', 'noti_cambio_actividades',
                               'noti_us_asignado','noti_cambio_estado_actividades',
                               'noti_creacion_proyecto','noti_creacion_equipos')}),
    )

# Register your models here.
admin.site.register(Usuario, MyUserAdmin)
