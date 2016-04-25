from django.contrib import admin
from .models import Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','is_active')

# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
