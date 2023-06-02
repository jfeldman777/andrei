from django.urls import path
from . import vvv
from . import db

urlpatterns = [
    path("form/<int:id>/", vvv.project_form, name="project_form_with_id"),
    path("form/", vvv.project_form, name="project_form"),
    path("smj/", db.smj, name="smj"),
    path("sm/", db.sm, name="sm"),
    path("s2/", db.s2, name="s2"),
    path("s1/", db.s1, name="s1"),
    path("sj/", db.sj, name="sj"),
    path("eva2/<str:fun>/", vvv.eva2, name="eva2"),
    path("b/<int:n>/", vvv.balance_map, name="balance_map"),
    path("ur/<int:p>/<int:r>/<int:j>/", vvv.assign_role, name="ur"),
    path("uj/<int:p>/<int:r>/<int:j>/", vvv.assign_project, name="uj"),
    path("ujr/<int:p>/<int:r>/<int:j>/", vvv.assign_role_project, name="ujr"),
    path("mr1/<int:p>/<int:r>/<int:j>/", vvv.available_role, name="mr1"),
    path("mr2/<int:p>/<int:r>/<int:j>/", vvv.rest_role, name="mr2"),
    path("mmj/<int:p>/<int:r>/<int:j>/", vvv.needs_project, name="mmj"),
    path("mmr/<int:p>/<int:r>/<int:j>/", vvv.needs_role, name="mmr"),
    path("mmjr/<int:p>/<int:r>/<int:j>/", vvv.needs_role_project, name="mmjr"),
    path("dj/<int:p>/<int:r>/<int:j>/", vvv.delta_project, name="dj"),
    path("aj/<int:p>/<int:r>/<int:j>/", vvv.all_project, name="aj"),
    path("dr/<int:p>/<int:r>/<int:j>/", vvv.delta_role, name="dr"),
    path("ar/<int:p>/<int:r>/<int:j>/", vvv.all_role, name="ar"),
    path("ajr/<int:p>/<int:r>/<int:j>/", vvv.all_role_project, name="ajr"),
    path("djr/<int:p>/<int:r>/<int:j>/", vvv.delta_role_project, name="djr"),
    path("mro/", vvv.rest_all, name="mro"),
    path("mrom/", vvv.available_all, name="mrom"),
    path("prjlist/", vvv.project_timeline, name="prjlist"),
    path("atj/", vvv.all_projects, name="atj"),
    path("atr/", vvv.all_resources, name="atr"),
    path("test/", vvv.atest, name="test"),
    path("", vvv.home, name="home"),
]
