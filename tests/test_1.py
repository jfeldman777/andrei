import pytest
from django.test import TestCase,Client
from mixer.backend.django import mixer
from django.urls import reverse,resolve
from jacob.vvv import *
from andrei2 import settings



@pytest.mark.django_db
def test_1():
    client = Client()
    response = client.get('/')
    assert response.status_code in (200, 301)
    
class sViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.names = [
            'alf',
            'mro',
            'mrom',
            'prjlist',
            'atj',
            'atr',
  
                    ]
        self.client = Client()

    def test_url_accessible_by_name(self):
        for name in self.names:
            print(2,name)
            response = self.client.get(reverse(name))
            self.assertIn(response.status_code, [200, 301])
    


