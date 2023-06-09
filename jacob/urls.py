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

    #path("keys_form/", view_forms.keys_form, name="keys_form"),

    path("grade_form/<int:pid>/<int:rid>/", view_forms.grade_form, name="grade_form"),
    

    path("save_max/", save_forms.save_max, name="save_max"),
    path("save_needs/", save_forms.save_needs, name="save_needs"),
    path("save_task/", save_forms.save_task, name="save_task"),
    

    #path("eva2/<str:fun>/", vvv.eva2, name="eva2"),
    
    
    path("b/<int:n>/", vvv.balance_map, name="balance_map"),
    
    
    path("tasks_r/<int:p>/<int:r>/<int:j>/", vvv.assign_role, name="ur"),
    path("tasks_j/<int:p>/<int:r>/<int:j>/", vvv.assign_project, name="uj"),
    path("tasks_jr/<int:p>/<int:r>/<int:j>/", vvv.assign_role_project, name="ujr"),

    
    path("needs_j/<int:p>/<int:r>/<int:j>/", vvv.needs_project, name="mmj"),
    path("needs_r/<int:p>/<int:r>/<int:j>/", vvv.needs_role, name="mmr"),
    path("needs_jr/<int:p>/<int:r>/<int:j>/", vvv.needs_role_project, name="mmjr"),
    
    path("delta_j/<int:p>/<int:r>/<int:j>/", vvv.delta_project, name="dj"),
    path("delta_r/<int:p>/<int:r>/<int:j>/", vvv.delta_role, name="dr"),
    path("delta_jr/<int:p>/<int:r>/<int:j>/", vvv.delta_role_project, name="djr"),
    
    
    path("balance_r/<int:p>/<int:r>/<int:j>/", vvv.all_role, name="ar"),
    path("balance_j/<int:p>/<int:r>/<int:j>/", vvv.all_project, name="aj"),
    path("balance_jr/<int:p>/<int:r>/<int:j>/", vvv.all_role_project, name="ajr"),
    
    
    path("max/", vvv.available_all, name="mrom"),
    path("max_r/<int:p>/<int:r>/<int:j>/", vvv.available_role, name="mr1"),
    path("rest_r/<int:p>/<int:r>/<int:j>/", vvv.rest_role, name="mr2"),
    path("rest/", vvv.rest_all, name="mro"),
 
    
    path("prjlist/", vvv.table_timeline, name="prjlist"),
    path("table_j/", vvv.table_projects, name="atj"),
    path("table_r/", vvv.table_resources, name="atr"),
    path("people/", vvv.people, name="people"),
    path("roles/", vvv.roles, name="roles"),
    
    path("test/", vvv.atest, name="test"),
    path("", vvv.home, name="home"),
]
