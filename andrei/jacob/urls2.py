from django.urls import path
from . import vvv

urlpatterns = [
    # path('prj_all/', vvv.prj_all, name='prj_all'),
    path('test1/<int:id>/', vvv.test1, name='test1'),
    path('left/<int:id>/', vvv.left, name='left'),
    path('prj_lead/', vvv.prj_lead, name='prj_lead'),
    path('res_lead/', vvv.res_lead, name='res_lead'),
    # path('jax3/', vvv.jax3, name='jax3'),
    # path('jax2/', vvv.jax2, name='jax2'),
    # path('ajax/', vvv.ajax, name='ajax'),

    # path('ajax0/', vvv.ajax0, name='ajax0'),
    path('res11/<int:r>/', vvv.res11, name='res11'),

    # path('page_balances/', vvv.page_balances, name='page_balances'),
    path('frames1prj/', vvv.frames1prj, name='frames1prj'),
    path('frames1res/', vvv.frames1res, name='frames1res'),
    path('otdlist/<int:i>/', vvv.otdlist, name='otdlist'),


     path('mytask/<int:id>/', vvv.mytask, name='mytask'),
    path('myotd1/<int:r>/', vvv.myotd1, name='myotd1'),
        path('myotd2/<int:r>/', vvv.myotd2, name='myotd2'),
    path('myotd3/<int:r>/', vvv.myotd3, name='myotd3'),

    path('prjlist/', vvv.projects, name='projects'),
    path('res/<int:id>/<int:r>/', vvv.res, name='res'),
    path('res01/<int:id>/<int:r>/', vvv.res01, name='res01'),
    path('res10/<int:id>/<int:r>/', vvv.res10, name='res10'),
    path('res_jr/<int:prj>/<int:r>/', vvv.res_jr, name='res_jr'),
    path('load/<int:id>/', vvv.load, name='load'),


    path('ostr/<int:id>/<int:r>/', vvv.ostr, name='ostr'),

    path('frames40', vvv.frames40, name='frames40'),
    path('frames42', vvv.frames42, name='frames42'),

    path('right', vvv.right, name='right'),
    path('entry/', vvv.entry, name='entry'),
    path('a3/<int:j>', vvv.a3, name='a3'),
    path('save2/', vvv.save2, name='save2'),
    path('save4/', vvv.save4, name='save4'),
    path('save3/', vvv.save3, name='save3'),
    path('a00/', vvv.a00, name='a00'),
    path('a2/<int:r>/', vvv.a2, name='a2'),
    path('a1/<int:j>/<int:r>/', vvv.a1, name='a1'),
    path('', vvv.a0, name='a0'),
]