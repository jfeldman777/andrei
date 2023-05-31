# myapp/tests.py
from django.test import TestCase, Client


class PageStatusTestCase(TestCase):
    def test_home_page_status(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)


#    def test_redirect_status(self):
#        client = Client()
#        response = client.get('/redirect-url/')
#        self.assertEqual(response.status_code, 301)
