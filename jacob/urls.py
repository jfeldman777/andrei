from django.urls import path
from . import vvv

urlpatterns = [
#        path('prjm_task/<int:p>/<int:r>/<int:j>/<int:y>/<int:m>', vvv.prjm_task, name='prjm_task'),
#            path('prm_isfree/<int:p>/<int:r>/<int:y>/<int:m>', vvv.prm_isfree, name='prm_isfree'),
#                path('rjm_load/<int:r>/<int:j>/<int:y>/<int:m>', vvv.rjm_load, name='rjm_load'),
#        path('prj_task/<int:p>/<int:r>/<int:j>', vvv.prj_task, name='prj_task'),
#            path('pr_isfree/<int:p>/<int:r>', vvv.pr_isfree, name='pr_isfree'),
#                path('rj_load/<int:r>/<int:j>', vvv.rj_load, name='rj_load'),
#                path('prm_task/<int:p>/<int:r>/<int:y>/<int:m>', vvv.prm_task, name='prm_task'),
#        path('pr_task/<int:p>/<int:r>', vvv.pr_task, name='pr_task'),
    

    
    
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
    path('smrom/', vvv.smrom, name='smrom'),
    path('mrom/', vvv.mrom, name='mrom'),
    path('prjlist/', vvv.prjlist, name='prjlist'),
    path('smj/', vvv.smj, name='smj'),
    path('smr/', vvv.smr, name='smr'),       
    path('s2/', vvv.s2, name='s2'),
    path('s1/', vvv.s1, name='s1'),    
    path('sj/', vvv.sj, name='sj'),
    path('atj/', vvv.atj, name='atj'),
    path('atr/', vvv.atr, name='atr'),
#    path('att/', vvv.att, name='att'),

    path('test/', vvv.atest, name='test'),

    path('', vvv.alf, name='alf'),
]
