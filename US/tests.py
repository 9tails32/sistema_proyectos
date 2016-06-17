from django.test import TestCase
from proyecto.models import Proyecto
from login.models import Usuario
from cliente.models import Cliente
from US.forms import *
from django.utils import timezone
from US.models import *
from equipo.models import Equipo
# Create your tests here.
class TestViewUS(TestCase):
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
        equipo = Equipo(proyecto=proyecto, nombre='equipo1')
        equipo.save()
        equipo.permisos={'1'}
        equipo.usuarios={'1'}
        equipo.save()

        tipo = TipoUS(pk=1, nombre='tipo')
        tipo.save()
        actividad = Actividades(pk=3, nombre='actividad', tipoUS=TipoUS.objects.get(pk=1))
        actividad.save()
        us = US(descripcion_corta='a', descripcion_larga='a', tiempo_planificado=3, valor_negocio=1,
                urgencia=1, tipoUS=tipo, usuario_asignado=Usuario.objects.get(pk=1), proyecto=proyecto)

        us.save()



    def test_create_tipo_template(self):

        resp = self.client.get('/us/tipo/create/')
        self.assertEqual(resp.status_code, 200)


    def test_create_tipo_form_valid(self):

        form=TipoUSForm({'nombre':'sprint 1'})
        self.assertTrue(form.is_valid())

    def test_detail_tipo(self):
        resp = self.client.get('/us/tipo/1/')
        self.assertEqual(resp.status_code, 200)

    def test_update_tipo_template(self):
        resp = self.client.get('/us/tipo/update/1/')
        self.assertEqual(resp.status_code, 200)

    def test_list_tipo(self):
        resp = self.client.get('/us/tipo/')
        self.assertEqual(resp.status_code, 200)

    def test_create_actividades_template(self):
        resp = self.client.get('/us/actividades/create/1/')
        self.assertEqual(resp.status_code, 200)

    def test_create_actividades_form_valid(self):
        form = ActividadesForm({'nombre': 'sprint 1'})
        self.assertTrue(form.is_valid())

    def test_delete_actividad_template(self):


        resp = self.client.get('/us/actividades/delete/3/')
        self.assertEqual(resp.status_code, 302)

    def test_list_actividades(self):
        resp = self.client.get('/us/actividades/1/')
        self.assertEqual(resp.status_code, 200)



    def test_create_us_form_valid(self):
        tipo = TipoUS(nombre='tipo')
        tipo.save()
        usuario = Usuario(username='asd',password='asdadsadasda')
        usuario.save()
        form = USForm({'descripcion_corta':'a', 'descripcion_larga':'a', 'tiempo_planificado':'3', 'valor_negocio':'1',
                'urgencia':'1', 'tipoUS': str(tipo.pk), 'usuario_asignado':str(usuario.pk)})
        self.assertFalse(form.is_valid())



    def test_check_actividad(self):
        tipo = TipoUS(pk=7, nombre='tipo')
        tipo.save()
        actividad = Actividades(pk=7, nombre='actividad', tipoUS=TipoUS.objects.get(pk=1))
        actividad.save()
        us = US(descripcion_corta='a', descripcion_larga='a', tiempo_planificado=3, valor_negocio=1,
                urgencia=1, tipoUS=TipoUS.objects.get(pk=7), usuario_asignado=Usuario.objects.get(pk=1),actividad=actividad)
        us.save()
        self.assertEqual(us.actividad, actividad)



    def test_cambiar_actividad_us_template(self):
        resp = self.client.get('/us/us/cambiar_actividad/1/')
        self.assertEqual(resp.status_code, 200)

    def test_cambiar_estado_actividad_us_template(self):
        resp = self.client.get('/us/us/cambiar_estado_actividad/1/')
        self.assertEqual(resp.status_code, 302)





