# myapp/tests.py
from django.test import TestCase, Client

class PageStatusTestCase(TestCase):
    def test_alf(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_mrom(self):
        client = Client()
        response = client.get('/mrom/')
        self.assertEqual(response.status_code, 200)        
    
    
    def test_mro(self):
        client = Client()
        response = client.get('/mro/')
        self.assertEqual(response.status_code, 200)   
        
    
    def test_atr(self):
        client = Client()
        response = client.get('/atr/')
        self.assertEqual(response.status_code, 200)        
        
    
    def test_prjlist(self):
        client = Client()
        response = client.get('/prjlist/')
        self.assertEqual(response.status_code, 200)    
        
    def test_ar(self):
        client = Client()
        response = client.get('/eva2/ar/')
        self.assertEqual(response.status_code, 200)            
 
    def test_dr(self):
        client = Client()
        response = client.get('/eva2/dr/')
        self.assertEqual(response.status_code, 200)     
        
    def test_aj(self):
        client = Client()
        response = client.get('/eva2/aj/')
        self.assertEqual(response.status_code, 200)            
 
    def test_dj(self):
        client = Client()
        response = client.get('/eva2/dj/')
        self.assertEqual(response.status_code, 200)      
        
        
    def test_ajr(self):
        client = Client()
        response = client.get('/eva2/ajr/')
        self.assertEqual(response.status_code, 200)            
 
    def test_djr(self):
        client = Client()
        response = client.get('/eva2/djr/')
        self.assertEqual(response.status_code, 200)           
    
#    def test_redirect_status(self):
#        client = Client()
#        response = client.get('/redirect-url/')
#        self.assertEqual(response.status_code, 301)
