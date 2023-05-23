#from django.test import TestCase
#
## Create your tests here.

from django.test import SimpleTestCase,TestCase,Client
from django.urls import reverse,resolve
from .vvv import *
class TestUrls(SimpleTestCase):
    def test_1(self):
        url = reverse('alf')
        print(resolve(url))
        self.assertEquals(resolve(url).func,alf)


    def test_ar(self):
        url = reverse('ar',args=[2,2,2])
        print(url)
        self.assertEquals(resolve(url).func, ar)


class TestVies(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_alf = reverse('alf')
        self.url_ar = reverse('ar',args = [2,2,2])

    def test_alf(self):
        response = self.client.get(self.url_alf)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'alf.html')
    def test_ar(self):
        response = self.client.get(self.url_ar)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'ar.html')
#
#
#
#
# #def runtests():
# #    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
# #
# #    from django.core.wsgi import get_wsgi_application
# #    application = get_wsgi_application()
# #
# #    from django.core.management import call_command
# #    result = call_command('test', 'userapp')
# #    sys.exit(result)
# from django.test import Client
#
# from django.http import response
# from django.test import TestCase, Client
#
# from .models import Load, Role, Project, UserProfile, Task
#
# class YourSystemTest(TestCase):
#     def setUp(self):
#         pass
#         # Настройка данных для тестов
#         # Создание объектов модели или другие необходимые действия перед каждым тестом
#
#     def tearDown(self):
#         pass
#         # Очистка данных после тестов
#         # Удаление созданных объектов или другие необходимые действия после каждого теста
#
#
#     # def test_atj(self):
#     #     client = Client()
#     #     response = client.get(reverse('atj'))
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_att(self):
#     #     client = Client()
#     #     response = client.get(reverse('att'))
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_alf(self):
#     #     client = Client()
#     #     response = client.get(reverse('alf'))
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_atr(self):
#     #     client = Client()
#     #     response = client.get(reverse('atr'))
#     #     self.assertEqual(response.status_code, 200)
#
# from django.test import TestCase
#
# # class MyPageTestCase(TestCase):
# #     def test_aj(self):
# #         response = self.client.get('http://127.0.0.1:8001/aj/2/2/2/')
# #         self.assertEqual(response.status_code, 200)
#     #
#     # def test_dj(self):
#     #     response = self.client.get('/dj/2/2/2/')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_ar(self):
#     #     response = self.client.get('/ar/2/2/2/')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_dr(self):
#     #     response = self.client.get('/dr/2/2/2/')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_ajr(self):
#     #     response = self.client.get('/ajr/2/2/2/')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_djr(self):
#     #     response = self.client.get('/djr/2/2/2/')
#     #     self.assertEqual(response.status_code, 200)
#
# from django.test import TestCase
# from .models import Project
#
# class MyTest(TestCase):
#     def setUp(self):
#         self.project = Project.objects.get(id=2)
#         print (self.project)
#
#     def test_aj(self):
#         response = self.client.get('/aj/2/2/2/')
#         self.assertEqual(response.status_code, 200)
