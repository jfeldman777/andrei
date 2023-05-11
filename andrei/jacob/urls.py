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
    path('sjr/', vvv.sjr, name='sjr'),
    path('sdr/', vvv.sdr, name='sdr'),
    path('sdjr/', vvv.sdjr, name='sdjr'),
    path('sr/', vvv.sr, name='sr'),
    path('test/', vvv.test, name='test'),
    path('sj/', vvv.sj, name='sj'),
    path('atj/', vvv.atj, name='atj'),
    path('atr/', vvv.atr, name='atr'),
    path('att/', vvv.att, name='att'),
    path('dr/<int:r>/', vvv.dr, name='dr'),
    path('ar/<int:r>/', vvv.ar, name='ar') ,
    path('ajr/<int:j>/<int:r>/', vvv.ajr, name='ajr'),
    path('djr/<int:j>/<int:r>/', vvv.djr, name='djr'),
    path('', vvv.alf, name='alf'),
]
