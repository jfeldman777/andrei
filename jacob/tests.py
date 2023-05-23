#from django.test import TestCase
#
## Create your tests here.
#
#def runtests():
#    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
#
#    from django.core.wsgi import get_wsgi_application
#    application = get_wsgi_application()
#
#    from django.core.management import call_command
#    result = call_command('test', 'userapp')
#    sys.exit(result)
from django.test import Client

from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from .models import Load, Role, Project, UserProfile, Task

class YourSystemTest(TestCase):
    def setUp(self):
        pass
        # Настройка данных для тестов
        # Создание объектов модели или другие необходимые действия перед каждым тестом

    def tearDown(self):
        pass
        # Очистка данных после тестов
        # Удаление созданных объектов или другие необходимые действия после каждого теста


    def test_atj(self):
        client = Client()
        response = client.get(reverse('atj'))
        self.assertEqual(response.status_code, 200)

    def test_att(self):
        client = Client()
        response = client.get(reverse('att'))
        self.assertEqual(response.status_code, 200)

    def test_alf(self):
        client = Client()
        response = client.get(reverse('alf'))
        self.assertEqual(response.status_code, 200)

    def test_atr(self):
        client = Client()
        response = client.get(reverse('atr'))
        self.assertEqual(response.status_code, 200)

from django.test import TestCase

class MyPageTestCase(TestCase):
    def test_aj(self):
        response = self.client.get('/aj/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)

    def test_dj(self):
        response = self.client.get('/dj/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)

    def test_ar(self):
        response = self.client.get('/ar/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)

    def test_dr(self):
        response = self.client.get('/dr/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)

    def test_ajr(self):
        response = self.client.get('/ajr/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)

    def test_djr(self):
        response = self.client.get('/djr/', {'p': 2, 'r': 2, "j":2})
        self.assertEqual(response.status_code, 200)
