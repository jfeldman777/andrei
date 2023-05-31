# myapp/tests.py
from django.test import TestCase, Client


class PageStatusTestCase(TestCase):
    def test_alf(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_mrom(self):
        client = Client()
        response = client.get("/mrom/")
        self.assertEqual(response.status_code, 200)

    def test_mro(self):
        client = Client()
        response = client.get("/mro/")
        self.assertEqual(response.status_code, 200)

    def test_atr(self):
        client = Client()
        response = client.get("/atr/")
        self.assertEqual(response.status_code, 200)

    def test_prjlist(self):
        client = Client()
        response = client.get("/prjlist/")
        self.assertEqual(response.status_code, 200)

    def test_ar(self):
        client = Client()
        response = client.get("/eva2/ar/")
        self.assertEqual(response.status_code, 200)

    def test_dr(self):
        client = Client()
        response = client.get("/eva2/dr/")
        self.assertEqual(response.status_code, 200)

    def test_aj(self):
        client = Client()
        response = client.get("/eva2/aj/")
        self.assertEqual(response.status_code, 200)

    def test_dj(self):
        client = Client()
        response = client.get("/eva2/dj/")
        self.assertEqual(response.status_code, 200)

    def test_ajr(self):
        client = Client()
        response = client.get("/eva2/ajr/")
        self.assertEqual(response.status_code, 200)

    def test_djr(self):
        client = Client()
        response = client.get("/eva2/djr/")
        self.assertEqual(response.status_code, 200)

    def test_uj(self):
        client = Client()
        response = client.get("/eva2/uj/")
        self.assertEqual(response.status_code, 200)

    def test_ur(self):
        client = Client()
        response = client.get("/eva2/ur/")
        self.assertEqual(response.status_code, 200)

    def test_ujr(self):
        client = Client()
        response = client.get("/eva2/ujr/")
        self.assertEqual(response.status_code, 200)

    def test_uj(self):
        client = Client()
        response = client.get("/eva2/uj/")
        self.assertEqual(response.status_code, 200)

    def test_mmjr(self):
        client = Client()
        response = client.get("/eva2/mmjr/")
        self.assertEqual(response.status_code, 200)

    def test_mmj(self):
        client = Client()
        response = client.get("/eva2/mmj/")
        self.assertEqual(response.status_code, 200)

    def test_mmr(self):
        client = Client()
        response = client.get("/eva2/mmr/")
        self.assertEqual(response.status_code, 200)

    def test_b(self):
        client = Client()
        response = client.get("/b/3/")
        self.assertEqual(response.status_code, 200)

    def test_mr1(self):
        client = Client()
        response = client.get("/eva2/mr1/")
        self.assertEqual(response.status_code, 200)
