from django.test import TestCase
from .models import Proyecto
from login.models import Usuario
from cliente.models import Cliente
from django.utils import timezone
from .forms import ProyectoForm
# Create your tests here.
class TestViewProyecto(TestCase):
    def test_list(self):
        resp = self.client.get('/proyecto/')
        self.assertEqual(resp.status_code, 200)

    def test_create_template(self):

        resp = self.client.get('/proyecto/create/')
        self.assertEqual(resp.status_code, 200)

    def test_create_form_valid(self):
        usuario = Usuario(username= 'user1', password= 'pass')
        cliente = Cliente(nombre='client1', direccion='Azara', email='asd@hotmail.com')
        cliente.save()
        usuario.save()
        form=ProyectoForm({'nombre':'proyecto', 'fecha_creacion':timezone.now(),
                             'fecha_fin':timezone.now(), 'fecha_inicio': timezone.now(),
                             'lider_proyecto':str(usuario.pk), 'cliente': str(cliente.pk),
                             'descripcion': 'Descripcion', 'estado': 'PEN',
                             'observaciones':'No hay observaciones'})
        self.assertTrue(form.is_valid())


    def test_create_form_invalid(self):
        usuario = Usuario(username='user1', password='pass')
        cliente = Cliente(nombre='client1', direccion='Azara', email='asd@hotmail.com')
        cliente.save()
        usuario.save()
        form = ProyectoForm({'nombre': 'proyecto', 'fecha_creacion': timezone.now(),
                             'fecha_fin': (timezone.now()-timezone.timedelta(days=1)), 'fecha_inicio': timezone.now(),
                             'lider_proyecto': str(usuario.pk), 'cliente': str(cliente.pk),
                             'descripcion': 'Descripcion', 'estado': 'PEN',
                             'observaciones': 'No hay observaciones'})
        self.assertFalse(form.is_valid())








