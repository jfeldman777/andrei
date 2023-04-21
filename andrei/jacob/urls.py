from django.urls import path
from . import views

urlpatterns = [

    path('projects', views.projects, name='projects'),
    path('people', views.people, name='people'),
    path('load/<int:id>/', views.load, name='load'),
    path('', views.index, name='index'),
]
