from django.forms import Form
from django.shortcuts import redirect

from .create_update import create_or_update_needs, create_or_update_task, create_or_update_res_max
from .models import Role, Project, UserProfile


def save_max(request):
    html = ""
    id = 1
    r = 1
    p = 1
    j = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        if form.is_valid():
            html = request.POST.get("html")
            for k, v in request.POST.items():
                if "." in k:
                    p, r, j, d = k.split(".")

                    try:
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)

                        create_or_update_res_max(person, role, d, v)
                    except:
                        pass
        else:
            print(form.errors)
    if html == "":
        return redirect(f"mr1/{p}/{r}/{j}/") #available_role(request, p, r, j)
    return redirect("mrom")#"available_all(request)  # s



def save_task(request):
    p = 0
    r = 0
    j = 0
    html = ""
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            for k, v in request.POST.items():
                html = request.POST.get("html")
                if "." in k:
                    p, r, j, d = k.split(".")
                    try:
                        project = Project.objects.get(id=j)
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)
                        create_or_update_task(
                            person, role, project, d, v
                        )  ##################################
                    except:
                        pass
        else:
            print(form.errors)

    return redirect(f"/{html}/{p}/{r}/{j}")


def save_needs(request):
    p = 0
    j = 0
    r = 0
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            for k, v in request.POST.items():
                html = request.POST.get("html")
                if "." in k:
                    p, r, j, d = k.split(".")

                    try:
                        person = None
                        role = Role.objects.get(id=r)
                        project = Project.objects.get(id=j)
                        create_or_update_needs(person, role, project, d, v)
                    except:
                        pass
        else:
            print(form.errors)

    return redirect(f"/{html}/{p}/{r}/{j}")
