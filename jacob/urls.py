from django.urls import path
from . import vvv

urlpatterns = [
    

    path('form/<int:id>/', vvv.alff, name='alff_with_id'),
    path('form/', vvv.alff, name='alff'),
    path('smj/', vvv.smj, name='smj'),
    path('sm/', vvv.sm, name='sm'),       
    path('s2/', vvv.s2, name='s2'),
    path('s1/', vvv.s1, name='s1'),    
    path('sj/', vvv.sj, name='sj'),

    path('eva2/<str:fun>/', vvv.eva2, name='eva2'), 
    
    path('b/<int:n>/', vvv.b, name='b'),        
    path('mjr/<int:p>/<int:r>/<int:j>/', vvv.mjr, name='mjr'),
    path('ur/<int:p>/<int:r>/<int:j>/', vvv.ur, name='ur'),
    path('uj/<int:p>/<int:r>/<int:j>/', vvv.uj, name='uj'),
    path('ujr/<int:p>/<int:r>/<int:j>/', vvv.ujr, name='ujr'),     
    path('mr1/<int:p>/<int:r>/<int:j>/', vvv.mr1, name='mr1'),
    path('mr2/<int:p>/<int:r>/<int:j>/', vvv.mr2, name='mr2'),
    path('mmj/<int:p>/<int:r>/<int:j>/', vvv.mmj, name='mmj'),
    path('mmr/<int:p>/<int:r>/<int:j>/', vvv.mmr, name='mmr'),
    path('mmjr/<int:p>/<int:r>/<int:j>/', vvv.mmjr, name='mmjr'),
    path('dj/<int:p>/<int:r>/<int:j>/', vvv.dj, name='dj'),
    path('aj/<int:p>/<int:r>/<int:j>/', vvv.aj, name='aj'),
    path('dr/<int:p>/<int:r>/<int:j>/', vvv.dr, name='dr'),
    path('ar/<int:p>/<int:r>/<int:j>/', vvv.ar, name='ar') ,
    path('ajr/<int:p>/<int:r>/<int:j>/', vvv.ajr, name='ajr'),
    path('djr/<int:p>/<int:r>/<int:j>/', vvv.djr, name='djr'),     
   
    path('mro/', vvv.mro, name='mro'),      
    path('mrom/', vvv.mrom, name='mrom'),
    path('prjlist/', vvv.prjlist, name='prjlist'), 
    path('atj/', vvv.atj, name='atj'),
    path('atr/', vvv.atr, name='atr'),
    path('test/', vvv.atest, name='test'),
    path('', vvv.alf, name='alf'),
]
