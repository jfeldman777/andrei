from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('e/', views.e, name='e'),
    path('', include('jacob.urls')),

]
