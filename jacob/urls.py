from django.urls import path
from . import vvv
from . import db

urlpatterns = [
    path("project_form/<int:id>/", vvv.project_form, name="project_form_with_id"),
    path("project_form/", vvv.project_form, name="project_form"),
    
    path("role_form/<int:id>/", vvv.role_form, name="role_form_with_id"),
    path("role_form/", vvv.role_form, name="role_form"),
    
    path("person_form/<int:id>/", vvv.person_form, name="person_form_with_id"),
    path("person_form/", vvv.create_user_and_profile, name="person_form"),

    path("keys_form/", vvv.keys_form, name="keys_form"),
    

    path("sm/", db.save_max, name="sm"),    
    path("s2/", db.save_needs, name="s2"),
    path("s1/", db.save_task, name="s1"),
    

    path("eva2/<str:fun>/", vvv.eva2, name="eva2"),
    
    
    path("b/<int:n>/", vvv.balance_map, name="balance_map"),
    
    
    path("ur/<int:p>/<int:r>/<int:j>/", vvv.assign_role, name="ur"),
    path("uj/<int:p>/<int:r>/<int:j>/", vvv.assign_project, name="uj"),
    path("ujr/<int:p>/<int:r>/<int:j>/", vvv.assign_role_project, name="ujr"), 

    
    path("mmj/<int:p>/<int:r>/<int:j>/", vvv.needs_project, name="mmj"),
    path("mmr/<int:p>/<int:r>/<int:j>/", vvv.needs_role, name="mmr"),
    path("mmjr/<int:p>/<int:r>/<int:j>/", vvv.needs_role_project, name="mmjr"),
    
    path("dj/<int:p>/<int:r>/<int:j>/", vvv.delta_project, name="dj"),  
    path("dr/<int:p>/<int:r>/<int:j>/", vvv.delta_role, name="dr"),
    path("djr/<int:p>/<int:r>/<int:j>/", vvv.delta_role_project, name="djr"),
    
    
    path("ar/<int:p>/<int:r>/<int:j>/", vvv.all_role, name="ar"),
    path("aj/<int:p>/<int:r>/<int:j>/", vvv.all_project, name="aj"),
    path("ajr/<int:p>/<int:r>/<int:j>/", vvv.all_role_project, name="ajr"),
    
    
    path("mrom/", vvv.available_all, name="mrom"),
    path("mr1/<int:p>/<int:r>/<int:j>/", vvv.available_role, name="mr1"),
    path("mr2/<int:p>/<int:r>/<int:j>/", vvv.rest_role, name="mr2"),
    path("mro/", vvv.rest_all, name="mro"),
 
    
    path("prjlist/", vvv.table_timline, name="prjlist"),
    path("atj/", vvv.table_projects, name="atj"),
    path("atr/", vvv.table_resources, name="atr"),
    path("people/", vvv.people, name="people"),
    path("roles/", vvv.roles, name="roles"),
    
    path("test/", vvv.atest, name="test"),
    path("", vvv.home, name="home"),
]
