from django.urls import path
from . import views, views2

urlpatterns = [
    path('upd/<int:project_id>/<int:person_id>/<int:year>/<int:month>/', views2.upd, name='upd'),
    path('projects', views.projects, name='projects'),
    path('people', views.people, name='people'),
    path('res/<int:id>/', views.res, name='res'),
    path('resp/<int:id>/', views.resp, name='resp'),
    path('res2/<int:prj>/<int:role>/<int:y>/<int:m>/', views2.res2, name='res2'),
    path('load/<int:id>/', views.load, name='load'),
    path('one2prj/', views2.one2prj, name='one2prj'),
    path('one2role/', views2.one2role, name='one2role'),
    path('load2/<int:prj>/<int:y>/<int:m>/', views2.load2, name='load2'),
    path('', views.index, name='index'),
]
