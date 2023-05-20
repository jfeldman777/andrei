from django.urls import path
from . import vvv

urlpatterns = [
        path('prjm_task/<int:p>/<int:r>/<int:j>/<int:y>/<int:m>', vvv.prjm_task, name='prjm_task'),
            path('prm_isfree/<int:p>/<int:r>/<int:y>/<int:m>', vvv.prm_isfree, name='prm_isfree'),
                path('rjm_load/<int:r>/<int:j>/<int:y>/<int:m>', vvv.rjm_load, name='rjm_load'),
        path('prj_task/<int:p>/<int:r>/<int:j>', vvv.prj_task, name='prj_task'),
            path('pr_isfree/<int:p>/<int:r>', vvv.pr_isfree, name='pr_isfree'),
                path('rj_load/<int:r>/<int:j>', vvv.rj_load, name='rj_load'),
                path('prm_task/<int:p>/<int:r>/<int:y>/<int:m>', vvv.prm_task, name='prm_task'),
        path('pr_task/<int:p>/<int:r>', vvv.pr_task, name='pr_task'),
    path('mro/', vvv.mro, name='mro'),
        path('smrom/', vvv.smrom, name='ssmrom'),
    path('mrom/', vvv.mrom, name='mrom'),
    path('prjlist/', vvv.prjlist, name='prjlist'),
    path('smj/', vvv.smj, name='smj'),

    path('smr/', vvv.smr, name='smr'),
    path('b/<int:n>/', vvv.b, name='b'),
    path('mr/<int:r>', vvv.mr, name='mr'),


    path('ur/<int:r>', vvv.ur, name='ur'),
    path('uj/<int:j>', vvv.uj, name='uj'),
    path('ujr/<int:j>/<int:r>/', vvv.ujr, name='ujr'), 
    
    path('mr1/<int:r>', vvv.mr1, name='mr1'),
    path('mr2/<int:r>', vvv.mr2, name='mr2'),
    path('mj/<int:j>', vvv.mj, name='mj'),

    path('dj/<int:j>', vvv.dj, name='dj'),
    path('aj/<int:j>', vvv.aj, name='aj'),
    path('s12/', vvv.s12, name='s12'),

    path('s11/', vvv.s11, name='s11'),
    path('s10/', vvv.s10, name='s10'),
    path('s9/', vvv.s9, name='s9'),
    path('s8/', vvv.s8, name='s8'),
    path('s7/', vvv.s7, name='s7'),
    path('s2/', vvv.s2, name='s2'),
    path('s1/', vvv.s1, name='s1'),
    path('s4/', vvv.s4, name='s4'),
    path('s3/', vvv.s3, name='s3'),

    path('s6/', vvv.s6, name='s6'),



    path('s5/', vvv.s5, name='s5'),
    path('test/', vvv.test, name='test'),
    path('sj/', vvv.sj, name='sj'),
    path('atj/', vvv.atj, name='atj'),
    path('atr/', vvv.atr, name='atr'),
    path('att/', vvv.att, name='att'),
    path('dr/<int:r>/', vvv.dr, name='dr'),
    path('ar/<int:r>/', vvv.ar, name='ar') ,
    path('ajr/<int:j>/<int:r>/', vvv.ajr, name='ajr'),
    path('djr/<int:j>/<int:r>/', vvv.djr, name='djr'),
    path('test/', vvv.test, name='test'),

    path('', vvv.alf, name='alf'),
]
