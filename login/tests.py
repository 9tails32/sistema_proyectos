from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class LoginViewTests (TestCase):

    def test_index(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_usuario_login_exitoso(self):
        usuario_activado= User.objects.create_user(username='usuario1', password='prueba123')
        usuario_activado.save()
        resp = self.client.post('/login/', {'username': 'usuario1', 'password': 'prueba123'})
        self.assertEqual(resp.context['state'], "Has iniciado sesion correctamente!")

    def test_usuario_login_no_activado(self):
        usuario_no_activado = User.objects.create_user(username='usuario2', password='prueba123')
        usuario_no_activado.is_active = False
        usuario_no_activado.save()
        resp = self.client.post('/login/', {'username': 'usuario2', 'password': 'prueba123'})
        self.assertEqual(resp.context['state'], "La cuenta no esta activa. Contacte con el administrador.")

    def test_usuario_inexistente(self):
        resp = self.client.post('/login/', {'username': 'usuario3', 'password': 'prueba123'})
        self.assertEqual(resp.context['state'], "Su nombre de usuario o password es incorrecto/a.")