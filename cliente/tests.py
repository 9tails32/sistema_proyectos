from django.test import TestCase
from .models import Cliente
from .forms import ClienteForm

# Create your tests here.
class ClienteViewTest(TestCase):
    def test_list(self):
        resp = self.client.get('/cliente/')
        self.assertEqual(resp.status_code, 302)

    def test_create(self):
        cliente = Cliente(pk=1, nombre='cliente', email='asdd@hotmail.com', direccion='azara')
        cliente.save()

        self.assertTrue(Cliente.objects.filter(nombre='cliente').exists())
        resp = self.client.post('/cliente/create/')
        self.assertEqual(resp.status_code, 302)

    def test_update(self):
        cliente=Cliente(pk=1, nombre='cliente')
        cliente.save()
        resp = self.client.post('/cliente/update/1')
        self.assertEqual(resp.status_code, 301)
        self.assertTrue(Cliente.objects.filter(nombre='cliente').exists())
