from django.urls import path
from . import vvv

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('ajax2/', vvv.ajax2, name='ajax2'),
    path('ajax/', vvv.ajax, name='ajax'),

    #path('page_projects/', vvv.index, name='page_projects'),
    #path('page_resources/', vvv.index, name='page_resources'),
    path('page_balances/', vvv.page_balances, name='page_balances'),
    #     # path('myprj/<int:id>/', views.myprj, name='myprj'),
    # path('upd/<int:project_id>/<int:person_id>/<int:year>/<int:month>/', views2.upd, name='upd'),
    # path('homeleft/', views.homeleft, name='homeleft'),
    # path('homeright/', views.homeright, name='homeright'),
    #
    # path('load2/<iFnt:prj>/<int:y>/<int:m>/', views2.load2, name='load2'),

    # path('res2/<int:prj>/<int:role>/<int:y>/<int:m>/', views2.res2, name='res2'),  path('prjlist/', views.prjlist, name='prjlist'),
    path('otdlist/', vvv.otdlist, name='otdlist'),

     path('mytask/<int:id>/', vvv.mytask, name='mytask'),

    path('myotd/<int:id>/', vvv.myotd, name='myotd'),

    path('projects', vvv.projects, name='projects'),

    # path('res_all/', views3.res_all, name='res_all'),
    path('res/<int:id>/<int:r>/', vvv.res, name='res'),
    path('res01/<int:id>/<int:r>/', vvv.res01, name='res01'),
    path('res10/<int:id>/<int:r>/', vvv.res10, name='res10'),
    # path('resp/<int:id>/', views3.resp, name='resp'),
    path('res_jr/<int:prj>/<int:r>/', vvv.res_jr, name='res_jr'),
    path('load/<int:id>/', vvv.load, name='load'),


    #path('one2prj/', vvv.one2prj, name='one2prj'),
    #path('one2role/', vvv.one2role, name='one2role'),

    path('ostr/<int:id>/<int:r>/', vvv.ostr, name='ostr'),
    #path('ost/', vvv.ostatok, name='ost'),
    #path('people/', vvv.people, name='people'),

    #path('details/', vvv.details, name='details'),

    path('frames40', vvv.frames40, name='frames40'),
    path('frames42', vvv.frames42, name='frames42'),
    path('left', vvv.left, name='left'),
    path('right', vvv.right, name='right'),
    path('entry/', vvv.entry, name='entry'),
    path('', vvv.index, name='index'),
]
