from django.urls import path
from . import vvv
from . import save_forms
from . import  view_forms

urlpatterns = [
    path("project_form/<int:id>/", view_forms.project_form, name="project_form_with_id"),
    path("project_form/", view_forms.project_form, name="project_form"),
    
    path("role_form/<int:id>/", view_forms.role_form, name="role_form_with_id"),
    path("role_form/", view_forms.role_form, name="role_form"),
    
    path("person_form/<int:id>/", view_forms.person_form, name="person_form_with_id"),
    path("person_form/", view_forms.create_user_and_profile, name="person_form"),

    path("keys_form/", view_forms.keys_form, name="keys_form"),

    path("grade_form/<int:pid>/<int:rid>/", view_forms.grade_form, name="grade_form"),
    

    path("sm/", save_forms.save_max, name="sm"),
    path("s2/", save_forms.save_needs, name="s2"),
    path("assign_workload/", save_forms.save_task, name="assign_workload"),
    

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
 
    
    path("prjlist/", vvv.table_timeline, name="prjlist"),
    path("atj/", vvv.table_projects, name="atj"),
    path("atr/", vvv.table_resources, name="atr"),
    path("people/", vvv.people, name="people"),
    path("roles/", vvv.roles, name="roles"),
    
    path("test/", vvv.atest, name="test"),
    path("", vvv.home, name="home"),
]
