from django.urls import path
from . import vvv

urlpatterns = [


    path('aj/<int:j>', vvv.aj, name='aj'),
    path('sjr/', vvv.sjr, name='sjr'),
    path('sr/', vvv.sr, name='srs'),
    path('test/', vvv.test, name='test'),
    path('sj/', vvv.sj, name='sj'),
    path('att/', vvv.att, name='att'),
    path('ar/<int:r>/', vvv.ar, name='ar'),
    path('ajr/<int:j>/<int:r>/', vvv.ajr, name='ajr'),
    path('', vvv.alf, name='alf'),
]
