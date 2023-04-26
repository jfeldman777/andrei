from django.shortcuts import render,redirect
from .models import Project, UserProfile, Load, Role, Task
import datetime,math

from django.forms import Form
def index(request):
    return render(request, 'index.html')

def people(request):
    people = UserProfile.objects.all()
    return render(request, 'people.html', {'people': people})

# def tasks(request):
#     form = None
#     return render(request, 'tasks.html',{form:form})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
from .forms import LoadForm, CellForm

#
# def load2(request, prj, y, m):
#     project = Project.objects.get(id=prj)
#     roles = Role.objects.all()
#     initial_data = []
#     for role in roles:
#         x={'role': role.id, 'project': prj, "month": f"{y}-{m}-15", "label": role.title}
#         loads = Load.objects.filter(role=role, project=prj, month=f"{y}-{m}-15")
#         if loads:
#             x['load']=loads[0].load
#         initial_data.append(x)
#
#
#     LoadFormSet = formset_factory(LoadForm, extra=0)
#     if request.method == "POST":
#         formset = LoadFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 role_id = form.cleaned_data["role"]
#                 load = form.cleaned_data["load"]
#                 Load.objects.update_or_create(
#                     role=role_id, project=project, month=f"{y}-{m}-15", defaults={"load": load}
#                 )
#         else:
#             print(formset.errors)
#         return redirect("load", prj)
#     else:
#         formset = LoadFormSet(initial=initial_data)
#     context = {"formset": formset, "project": project, "month": f"{y}-{m}"}
#     return render(request, "load2.html", context)

###########################################
def one2prj(request):
    people = UserProfile.objects.all().order_by('role', 'user')
    projects = Project.objects.all().order_by('start_date')
    one = []
    for person in people:
        one.append(person.user.last_name)
        for project in projects:
            ps = list(project.people.all())
            if person in ps:
                one.append(1)
            else:
                one.append(0)

    return render(request,"one2prj.html",{'people':people, 'projects':projects, "one":one},)

def one2role(request):
    roles = Role.objects.all()
    people = UserProfile.objects.all().order_by('role','user')

    return render(request,"one2role.html",{'roles':roles,'people':people},)