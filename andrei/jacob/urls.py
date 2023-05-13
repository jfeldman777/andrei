from django.urls import path
from . import vvv

urlpatterns = [
    path('mro/', vvv.mro, name='mro'),
    path('prjlist/', vvv.projects, name='projects'),
    path('smj/', vvv.smj, name='smj'),
    path('smr/', vvv.smr, name='smr'),
    path('mr/<int:r>', vvv.mr, name='mr'),
    path('mj/<int:j>', vvv.mj, name='mj'),
    path('dj/<int:j>', vvv.dj, name='dj'),
    path('aj/<int:j>', vvv.aj, name='aj'),

    path('s2/', vvv.s2, name='s2'),
    path('s1/', vvv.s1, name='s1'),
    path('s4/', vvv.s4, name='s4'),
    path('s3/', vvv.s3, name='s3'),

    path('s6/', vvv.s6, name='s6'),
    # path('sdrd/', vvv.sdrd, name='sdrd'),



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
