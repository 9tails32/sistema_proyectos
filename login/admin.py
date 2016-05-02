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
            (None, {'fields': ('cedula','direccion','formato_notificaciones','hora_notificaciones','noti_creacion_proyecto','noti_creacion_usuario','noti_creacion_equipos')}),
    )

# Register your models here.
admin.site.register(Usuario, MyUserAdmin)
