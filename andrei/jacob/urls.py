from django.urls import path
from . import views, views2,views3,v

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('ajax2/', views2.ajax2, name='ajax2'),
    path('ajax/', views2.ajax, name='ajax'),
    #     # path('myprj/<int:id>/', views.myprj, name='myprj'),
    # path('upd/<int:project_id>/<int:person_id>/<int:year>/<int:month>/', views2.upd, name='upd'),
    # path('homeleft/', views.homeleft, name='homeleft'),
    # path('homeright/', views.homeright, name='homeright'),
    #
    # path('load2/<iFnt:prj>/<int:y>/<int:m>/', views2.load2, name='load2'),

    # path('res2/<int:prj>/<int:role>/<int:y>/<int:m>/', views2.res2, name='res2'),  path('prjlist/', views.prjlist, name='prjlist'),
    path('otdlist/', views.otdlist, name='otdlist'),

     path('mytask/<int:id>/', views3.mytask, name='mytask'),

    path('myotd/<int:id>/', views.myotd, name='myotd'),

    path('projects', views3.projects, name='projects'),

    # path('res_all/', views3.res_all, name='res_all'),
    path('res/<int:id>/<int:r>/', views3.res, name='res'),
    path('res01/<int:id>/<int:r>/', views3.res01, name='res01'),
    path('res10/<int:id>/<int:r>/', views3.res10, name='res10'),
    # path('resp/<int:id>/', views3.resp, name='resp'),
    path('res_jr/<int:prj>/<int:r>/', views3.res_jr, name='res_jr'),
    path('load/<int:id>/', views3.load, name='load'),


    path('one2prj/', views.one2prj, name='one2prj'),
    path('one2role/', views.one2role, name='one2role'),

    path('ostr/<int:r>/', views.ostr, name='ostr'),
    path('ost/', views.ostatok, name='ost'),
    path('people/', views2.people, name='people'),

    path('details/', views.details, name='details'),

    path('frames40', v.frames40, name='frames40'),
    path('frames42', v.frames42, name='frames42'),
    path('left', v.left, name='left'),
    path('right', v.right, name='right'),
    path('', v.entry, name='entry'),
]
