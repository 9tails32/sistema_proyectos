from django.test import TestCase
from login.models import Usuario as User

# Create your tests here.

class LoginViewTests (TestCase):
    """Pruebas para la pantalla de login."""
    def test_index(self):
        """
        Prueba para comprobar la conexion con el template de login.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)

    def test_logout(self):
        """
        Prueba para comprobar la conexion cuando el usuario ingreso sesion.
        """
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_usuario_login_exitoso(self):
        """
        Prueba de login exitoso.
        """
        usuario_activado= User.objects.create_user(username='usuario1', password='prueba123')
        usuario_activado.save()
        resp = self.client.post('/login/', {'username': 'usuario1', 'password': 'prueba123'})

        self.assertEqual(resp.status_code, 302)

    def test_usuario_login_no_activado(self):
        """
        Prueba de usuario no activado intentando ingresar.
        """
        usuario_no_activado = User.objects.create_user(username='usuario2', password='prueba123')
        usuario_no_activado.is_active = False
        usuario_no_activado.save()
        resp = self.client.post('/login/', {'username': 'usuario2', 'password': 'prueba123'})
        self.assertEqual(resp.context['state'], "La cuenta no esta activa. Contacte con el administrador.")

    def test_usuario_inexistente(self):
        """
        Prueba de usuario no existente intentando ingresar
        """
        resp = self.client.post('/login/', {'username': 'usuario3', 'password': 'prueba123'})
        self.assertEqual(resp.context['state'], "Su nombre de usuario o password es incorrecto/a.")