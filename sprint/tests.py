from django.test import TestCase
from proyecto.models import Proyecto
from login.models import Usuario
from cliente.models import Cliente
from sprint.models import Sprint
from sprint.forms import SprintForm, AsignarUSForm
from django.utils import timezone
from US.models import *

# Create your tests here.
class TestViewSprint(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(username='user1', email='asd@asd.com',password='mangekyou', is_staff=True,is_superuser=True)
        cliente = Cliente(nombre='client1', direccion='Azara', email='asd@hotmail.com')
        cliente.save()
        usuario.save()
        self.client.login(username='user1',password='mangekyou')
        proyecto=Proyecto(id=1,nombre='proyecto',
                             fecha_fin=timezone.now(), fecha_inicio=timezone.now(),
                             lider_proyecto=usuario, cliente=cliente,
                             descripcion= 'Descripcion',
                             )
        proyecto.save()





    def test_create_template(self):

        resp = self.client.get('/sprint/create/1/')
        self.assertEqual(resp.status_code, 200)

    def test_create_form_valid(self):

        form=SprintForm({'nombre':'sprint 1', 'fecha_inicio': timezone.now()})
        self.assertTrue(form.is_valid())
        resp = self.client.post('/sprint/create/1/',{'form':form})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(form.is_valid())


    def test_create_no_proyect(self):

        resp = self.client.post('/sprint/create/2/')
        self.assertEqual(resp.status_code, 302)

    def test_detail(self):
        resp = self.client.post('/sprint/1/')
        self.assertEqual(resp.status_code, 302)

    def test_asignarUS(self):
        sprint = Sprint(id=3, nombre='sprint 3', fecha_inicio= timezone.now(),proyecto=Proyecto.objects.get(pk=1))
        sprint.save()
        tipo = TipoUS(nombre='tipo')
        tipo.save()
        us = US(descripcion_corta='a', descripcion_larga='a', tiempo_planificado=3, valor_negocio=1,
                urgencia=1, tipoUS=tipo, usuario_asignado=Usuario.objects.get(pk=1))
        us.save()
        sprint.duracion = 3
        sprint.save()
        resp = self.client.post('/sprint/asignar_us/3')
        self.assertEqual(resp.status_code, 301)

