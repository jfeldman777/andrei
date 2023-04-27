from django.urls import path
from . import views, views2,views3

urlpatterns = [
    path('load5/', views3.ajax2, name='ajax2'),
    path('load4/', views3.ajax, name='ajax'),
    #
    # path('upd/<int:project_id>/<int:person_id>/<int:year>/<int:month>/', views2.upd, name='upd'),
    path('projects', views3.projects, name='projects'),

    path('res/<int:id>/', views3.res, name='res'),
    path('resp/<int:id>/', views3.resp, name='resp'),
    # path('res2/<int:prj>/<int:role>/<int:y>/<int:m>/', views2.res2, name='res2'),
    path('load/<int:id>/', views3.load, name='load'),
    #
    # path('load2/<int:prj>/<int:y>/<int:m>/', views2.load2, name='load2'),

    path('one2prj/', views.one2prj, name='one2prj'),
    path('one2role/', views.one2role, name='one2role'),

    path('ost/', views.ostatok, name='ost'),
    path('people/', views.people, name='people'),
    path('', views.index, name='index'),
]
