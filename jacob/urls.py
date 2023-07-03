from django.urls import path
from . import vvv, export
from . import save_forms
from . import  view_forms
from .BalanceView import BalanceView


urlpatterns = [
    path("project_form/<int:id>/", view_forms.project_form, name="project_form_with_id"),
    path("project_form/", view_forms.project_form, name="project_form"),

    path("balance/<int:id>/<int:coord>/<int:mod>/", BalanceView.as_view()),



    path("role_form/<int:id>/", view_forms.role_form, name="role_form_with_id"),
    path("role_form/", view_forms.role_form, name="role_form"),
    
    path("person_form/<int:id>/", view_forms.person_form, name="person_form_with_id"),
    path("person_form/", view_forms.create_user_and_profile, name="person_form"),



    path("grade_form/<int:pid>/<int:rid>/", view_forms.grade_form, name="grade_form"),
    

    path("save_max/", save_forms.save_max, name="save_max"),
    path("save_needs/", save_forms.save_needs, name="save_needs"),
    path("save_task/", save_forms.save_task, name="save_task"),
    path("save_wish/", save_forms.save_wish, name="save_wish"),


    
    path("b/<int:n>/", vvv.balance_map, name="balance_map"),
    

    
    
    path("export_prj/", export.prj2),
    path("export_plan/<int:id>/<int:coord>/<int:mod>/", export.export_plan),

    path("max/", vvv.available_all),
    # path("max/<str:msg>/", vvv.available_all),

    path("max_r/<int:r>/", vvv.available_role),

    path("rest/", vvv.rest_all),
    path("rest_r/<int:r>/", vvv.rest_role),
 
    
    path("prjlist/", vvv.table_timeline, name="prjlist"),
    path("tab_j/", vvv.table_projects, name="atj"),
    path("tab_r/", vvv.table_resources, name="atr"),
    path("people/", vvv.people, name="people"),
    path("roles/", vvv.roles, name="roles"),

    path("test2/", view_forms.atest2, name="test2"),
    path("test1/", vvv.atest1, name="test1"),
    path("test/", vvv.atest, name="test"),
    path("", vvv.home, name="home"),
    path("accounts/profile/", vvv.home, name="home"),
]
