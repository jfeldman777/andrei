from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
from .forms import LoadForm, CellForm
from .views3 import *
from .views import *
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

from django.shortcuts import render
from .forms import TableCellForm, table_to_formset

def table_formset_view(request):
    table = []
    # Replace with your own method of obtaining table data
    formset = table_to_formset(table)
    if request.method == 'POST':
        formset = TableCellForm(request.POST)
        if formset.is_valid():
            # Handle form submission
            pass
    return render(request, 'table_formset.html', {'formset': formset})

def ajax(request):
    id = 1
    roles = list(Role.objects.all().order_by('id'))
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #id = form.cleaned_data["id"]
            id = int(request.POST.get('id'))
            project = Project.objects.get(id=id)
            for k,v in request.POST.items():
                if '.' in k:
                    ki,m=k.split('.')
                    ri = int(ki)
                    role = Role.objects.get(id=ri)
                    l = float(v)
                    print(project,role,m,l)
                    updateORcreateL(project,role,m,l)

        else:
            print(form.errors)

    return redirect("load",id)

def ajax2(request):
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sid = request.POST.get('id')
            id = int(sid)
            project = Project.objects.get(id=id)
            for k,v in request.POST.items():
                if '.' in k:
                    p,ms,r=k.split('.')
                    person = UserProfile.objects.get(id=p)
                    updateORcreate(person,id,ms,float(v))
        else:
            print(form.errors)

    return redirect("res_jr",id,r)

def people(request):
    people = UserProfile.objects.all().order_by("role")
    t12 = ['Роль','Фамилия','Имя']+t12ym()
    data = [([p.role,p.user.last_name,p.user.first_name]+[1]*12) for p in people]
    data1 = [([0,0,0]+[1]*12) for p in people]
    n = 0
    for p in people:
        less = Less.objects.all().filter(person = p)
        for l in less:
            data = correct(data,l,n)
        n+=1

    k = 0
    for p in people:
        d = datetime.now().date()
        sum = 0
        for i in range(12):
            t = tasks(p.id,d)
            d = inc(d)
            if(t>0):

                data[k][i+3]={"d":data[k][i+3],"t":t}
        print(k, i,data[k][i+3] )
        k+=1
    return render(request, 'people.html', {'people': people,"t12":t12,"data":data})