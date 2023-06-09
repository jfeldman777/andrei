from django.forms import Form
from django.shortcuts import redirect

from .create_update import create_or_update_needs, create_or_update_workload, create_or_update_res_max, \
    create_or_update_wish
from .models import Role, Project, UserProfile
from .timing import timing_decorator


@timing_decorator
def save_max(request):
    msg=""
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
                        print("bad",person,role,d,v)
        else:
            print(form.errors)

    return redirect(html)#"available_all(request)  # s


@timing_decorator
def save_task(request):
    print(787)
    p = 0
    r = 0
    j = 0
    html = ""
    if request.method == "POST":
        form = Form(request.POST)
        print(788)
        if form.is_valid():
            html = request.POST.get("html")
            for k, v in request.POST.items():
                if "." in k:
                    p, r, j, d = k.split(".")
                    print(k,111,v)
                    try:
                        project = Project.objects.get(id=j)
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)

                        print(898,v)
                        create_or_update_workload(
                            person, role, project, d, v
                        )  ##################################
                    except:
                        pass
        else:
            print(form.errors)

    return redirect(html)

@timing_decorator
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
                    print(987,p,r,j,d)
                    try:
                        person = None
                        role = Role.objects.get(id=r)
                        project = Project.objects.get(id=j)
                        create_or_update_needs(person, role, project, d, v)
                    except:
                        pass
        else:
            print(form.errors)
    print(html)
    return redirect(html)


@timing_decorator
def save_wish(request):
    html=''
    j = 0
    r = 0
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
             html = request.POST.get("html")
             r =  request.POST.get("role")
             j =  request.POST.get("project")
             v =  request.POST.get("wish")
             try:
                role = Role.objects.get(id=r)
                project = Project.objects.get(id=j)
                assert isinstance(v, str)
                create_or_update_wish(role, project, v)
             except:
                pass
        else:
            print(form.errors)
            return  form.errors
    return "OK"
    #return redirect(f"/{html}/{p}/{r}/{j}")

