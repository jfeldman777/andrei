from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory
from .models import Load, Role, Project, UserProfile, Task
from .forms import LoadForm, CellForm


def load2(request, prj, y, m):
    project = Project.objects.get(id=prj)
    roles = Role.objects.all()
    initial_data = []
    for role in roles:
        x={'role': role.id, 'project': prj, "month": f"{y}-{m}-15", "label": role.title}
        loads = Load.objects.filter(role=role, project=prj, month=f"{y}-{m}-15")
        if loads:
            x['load']=loads[0].load
        initial_data.append(x)

    print(initial_data)
    LoadFormSet = formset_factory(LoadForm, extra=0)
    if request.method == "POST":
        formset = LoadFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                role_id = form.cleaned_data["role"]
                load = form.cleaned_data["load"]
                Load.objects.update_or_create(
                    role_id=role_id, project=project, month=f"{y}-{m}-15", defaults={"load": load}
                )
        else:
            print(formset.errors)
        return redirect("load", prj)
    else:
        formset = LoadFormSet(initial=initial_data)
    context = {"formset": formset, "project": project, "month": f"{y}-{m}"}
    return render(request, "load2.html", context)

###########################################
def one2prj(request):
    people = UserProfile.objects.all().order_by('role', 'user')
    projects = Project.objects.all().order_by('start_date')
    one = []
    for person in people:
        one.append(person.user.last_name)
        for project in projects:
            ps = list(project.people.all())
            if person.user in ps:
                one.append(1)
            else:
                one.append(0)
        mypeople = UserProfile.objects.all().order_by('role', 'user')

    return render(request,"one2prj.html",{'people':people, 'projects':projects, "one":one},)

def one2role(request):
    roles = Role.objects.all()
    people = UserProfile.objects.all().order_by('role','user')

    return render(request,"one2role.html",{'roles':roles,'people':people},)
######################################################################

def res2(request,prj,role,y,m):
    project = Project.objects.get(id=prj)
    people = project.people.filter(role = role)

    initial_data = []
    for user in people:
        loads = Task.objects.filter(role=role, project=prj, month=f"{y}-{m}-15")
        initial_data.append({"role": role.id, 'project': prj,
                             "month": f"{y}-{m}-15","person":user.id,
                             "label": user.last_name})
        if loads:
            initial_data.append({"load": loads[0].load,})

    LoadFormSet = formset_factory(CellForm, extra=0)
    if request.method == "POST":
        formset = LoadFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                role_id = form.cleaned_data["role"]
                load = form.cleaned_data["load"]
                person = form.cleaned_data["person"]
                Task.objects.update_or_create(
                   role_id=role_id, project=project, month=f"{y}-{m}-15", defaults={"load": load},
                   person = person
                )
        else:
            print(formset.errors)
        return redirect("res", prj)
    else:
        formset = LoadFormSet(initial=initial_data)
    context = {"formset": formset, "project": project, "month": f"{y}-{m}", }
    return render(request, "res2.html", context)

# views.py
from django.shortcuts import render, redirect
from .forms import UpdateFloatForm
from .models import Task
import datetime


def upd(request, project_id, person_id, year, month):
    d = datetime.date(year=int(year), month=int(month), day=15)
    try:
        load = Task.objects.get(person=person_id, project=project_id, month=d).load
    except Task.DoesNotExist:
        load = None
    if request.method == 'POST':
        form = UpdateFloatForm(request.POST)
        if form.is_valid():
            Task.objects.update_or_create(
                person_id=person_id,
                project_id=project_id,
                month=d,
                defaults={'load': form.cleaned_data['load']}
            )
        else:
            print(form.errors)
        return redirect("resp", project_id)
    else:
        form = UpdateFloatForm(initial={
            'person_id': person_id,
            'project_id': project_id,
            'year': year,
            'month': month,
            'load': load
        })
        project = Project.objects.get(id=project_id)
        person = UserProfile.objects.get(id=person_id).user.last_name

    return render(request, 'upd.html', {'form': form,'project':project,'person':person,
                                        'month':f"{month}-{year}"})
