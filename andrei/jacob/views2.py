from django.shortcuts import render,redirect
from django.forms import formset_factory
from .models import Load, Role, Project
from .forms import LoadForm

def load2(request, prj, y, m):
    project = Project.objects.get(id=prj)
    roles = Role.objects.all()
    initial_data = []
    for role in roles:
        loads = Load.objects.filter(role=role, project=prj, month=f"{y}-{m}-15")
        if loads:
            initial_data.append({"load": loads[0].load,'role':role.id,'project':prj,"month":f"{y}-{m}-15","label":role.title})
        else:
            initial_data.append({"load":0,"role":role.id,'project':prj,"month":f"{y}-{m}-15","label":role.title})
    LoadFormSet = formset_factory(LoadForm, extra=0)
    if request.method == "POST":
        formset = LoadFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.fields)
                role_id = form.cleaned_data["role"]
                load = form.cleaned_data["load"]
                Load.objects.update_or_create(
                    role_id=role_id, project=project, month=f"{y}-{m}-15", defaults={"load": load}
                )
        else:
            print(formset.errors)
        return redirect("load", prj)
    else:
        print(initial_data)
        formset = LoadFormSet(initial=initial_data)
    context = {"formset": formset, "project": project, "month": f"{y}-{m}"}
    return render(request, "load2.html", context)

