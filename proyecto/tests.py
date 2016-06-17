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
        self.assertEqual(resp.status_code, 302)

    def test_create_template(self):

        resp = self.client.get('/proyecto/create/')
        self.assertEqual(resp.status_code, 302)

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

    def test_log(self):
        usuario = Usuario.objects.create_user(username='user1', email='asd@asd.com', password='mangekyou',
                                              is_staff=True, is_superuser=True)
        cliente = Cliente(nombre='client1', direccion='Azara', email='asd@hotmail.com')
        cliente.save()
        usuario.save()
        self.client.login(username='user1', password='mangekyou')
        proyecto = Proyecto(id=1, nombre='proyecto',
                            fecha_fin=timezone.now(), fecha_inicio=timezone.now(),
                            lider_proyecto=usuario, cliente=cliente,
                            descripcion='Descripcion',
                            )
        proyecto.save()
        resp = self.client.get('/proyecto/log_proyecto/1')
        self.assertEqual(resp.status_code, 301)







