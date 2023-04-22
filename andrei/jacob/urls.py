from django.urls import path
from . import views, views2

urlpatterns = [

    path('projects', views.projects, name='projects'),
    path('people', views.people, name='people'),
    path('load/<int:id>/', views.load, name='load'),
    path('one2prj/', views2.one2prj, name='one2prj'),
    path('one2role/', views2.one2role, name='one2role'),
    path('load2/<int:prj>/<int:y>/<int:m>/', views2.load2, name='load2'),
    path('', views.index, name='index'),
]
