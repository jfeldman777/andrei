from django.shortcuts import redirect, get_object_or_404

from .db import delta_role_project_12, needs_role_project_12, person_more_100_12, task_role_project_12
from .db import get_prj_triplet, rest_of_time_pr_12, time_available_person_role_12
from .db import task_person_role_project_12, real_and_virtual_people, real_people
from .utils import *
from datetime import date
from .models import UserProfile


from django.urls import resolve


'''
отсюда можно запускать тесты
'''
def atest(request:object)->object:
    a = outsrc(2, 2)
    b = vacancia(2, 2)

    return render(request, "a_test.html", {"a": a, "b": b})

def a00(request:object)->object:
    return render(request, "a00.html")


'''
домашняя страница
'''
def home(request):
    return render(request, "x_home.html", {})


'''
Объект Вакансия - загрузка на год
'''
def vacancia(role:object, project:object)->List[int]:
    person = None
    person = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]  ##АУТСОРС
    return task_person_role_project_12(person, role, project)

'''
Объект Аутсорс - загрузка на год
'''
def outsrc(role:object, project:object)->List[int]:
    person = None
    try:
        person = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        pass
    return task_person_role_project_12(person, role, project)




def delta_on_span(r, j, n):
    rjd = delta_role_project_12(r, j)
    sum = 0
    for i in range(n):
        if rjd[i] < 0:
            sum -= rjd[i]
    return sum

'''
НЕехватка ресурсов - роль - проект - время-месяцев - суммарно по месяцам
'''
def needs_on_span(r:object, j:object, n:int)->int:
    rjd = needs_role_project_12(-1,r, j)
    sum = 0
    for i in range(n):
        sum += rjd[i]
    if sum == 0:
        return 1 #чтобы не делить на ноль
    return sum

'''
вход в балансы за х месяцев
'''

def balance_map(request:object, n:int)->object:
    projects = Project.objects.all()
    roles = Role.objects.all()
    xy = [0] * len(projects)
    for i in range(len(projects)):
        xy[i] = [0] * (len(roles) + 1)

    txy = [0] * len(roles)
    for j in range(len(roles)):
        txy[j] = {"val": roles[j].title, "link": f"/dr/0/{roles[j].id}/0/"}

    for i in range(len(projects)):
        xy[i][0] = {"val": projects[i], "link": f"/dj/0/0/{projects[i].id}/"}
        for j in range(len(roles)):
            project = projects[i]
            role = roles[j]
            x = round(100 * delta_on_span(role, project, n) / needs_on_span(role, project, n))

            if 20 > x > 0:
                color = "yellow"
            elif x >= 20:
                color = "pink"
            else:
                color = "white"

            xy[i][j + 1] = {
                "val": f"{x}%",
                "link": f"/djr/0/{roles[j].id}/{projects[i].id}/",
                "color": color,
                "i": project.id,
                "j": role.id,
            }
    context = {"tab": xy, "txy": txy, "n": n, "hh": n2txt(n)}

    return render(request, "b.html", context)

'''
форма для изменение или создания роли (если номер не указан)
'''
def role_form(request, id=None):
    instance = None
    if id:
        instance = get_object_or_404(Role, id=id)

    if request.method == "POST":
        form = RoleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("roles")

    else:
        form = RoleForm(instance=instance)
    return render(request, "form.html", {"form": form,"title":"Роль"})
'''
форма для изменение или создания проекта (если номер не указан)
'''


from .forms import ProjectForm

def project_form(request, id=None):
    instance = None
    if id:
        instance = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("prjlist")
    else:
        initial_data = {}
        if instance is not None:
            initial_data = {'general': instance.general.fio}
        form = ProjectForm(instance=instance, initial=initial_data)

    return render(request, "form.html", {"form": form,"title":"Проект"})






'''
форма для изменение или создания человека (если номер не указан)
'''
def person_form(request, id):
    instance = None
    if id:
        instance = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":
        form = User2Form(request.POST, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            user.role_id = form.cleaned_data['role'].id  # Set the foreign key using an ID
            user.save()
            user.res.set(form.cleaned_data['res'])  # Set the many-to-many relationship
            user.save()
            return redirect("people")
    else:
        form = User2Form(instance=instance)
    return render(request, "form.html",  {"form": form,"title":"Сотрудник"})

from .forms import UserAndProfileForm, RoleForm, User2Form, KeysForm, ProjectForm


def create_user_and_profile(request):
    if request.method == 'POST':
        form = UserAndProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            user_profile = UserProfile.objects.create(user=user,
                                                      role=form.cleaned_data['role'],
                                                      fio=form.cleaned_data['fio'],
                                                     )
            selected_roles = form.cleaned_data.get('res', [])
            user_profile.res.set(selected_roles)

            return redirect("people")



    else:
        form = UserAndProfileForm()

    return render(request, 'form.html', {'form': form})




def keys_form(request, id=None):
    instance = None
    if request.method == "POST":
        form = KeysForm(request.POST, instance=instance)
        if form.is_valid():
            user_profile = form.save(commit=False)
            selected_roles = form.cleaned_data.get('res', None)

            if selected_roles is not None:
                if not isinstance(selected_roles, list):
                    selected_roles = [selected_roles]

                user_profile.res.set(selected_roles)

            return redirect("people")
    else:
        form = KeysForm()
    return render(request, "form.html",  {"form": form, "title": "Сотрудник"})
'''
Все проекты в одной таблице

'''

def table_projects(request:object)->object:
    projects = Project.objects.all().order_by("general")
    data = []
    for p in projects:
        x = {"j": p.id, "project": p.title, "name": p.general.fio}
        data.append(x)
    context = {"data": data}

    return render(request, "atj.html", context)

'''
Все ресурсы в одной таблице
'''
def table_resources(request:object)->object:
    context = {}
    roles = Role.objects.all().order_by("general")
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {"title": p.title, "r": p.id, "name": u.fio}
        data2.append(x)
    context["data2"] = data2

    return render(request, "atr.html", context)
def people(request:object)->object:
    context = {}
    people = UserProfile.objects.filter(virtual='False').order_by("fio")
    data2 = []
    for p in people:
        x = {"fio": p.fio, "role": p.role, "res": p.res.all,"id":p.id}
        data2.append(x)
    context["data2"] = data2

    return render(request, "people.html", context)

def roles(request:object)->object:
    context = {}
    roles = Role.objects.all().order_by("general")
    data2 = []
    for p in roles:
        x = {"title": p.title, "id": p.id, "general": p.general.userprofile.fio}
        data2.append(x)
    context["data2"] = data2

    return render(request, "roles.html", context)



'''
Заголовок - 12 месяцев
'''
def moon()->List[object]:
    y_data = []
    m_data = []
    ym = []
    d = date0()
    for i in range(12):
        y_data.append(d.year)
        m_data.append(d.month)
        ym.append({"y": d.year, "m": d.month})
        d = inc(d)
    return {"yy": y_data, "mm": m_data, "ym": ym}
    ##################################################################

'''
назначения - один ресурс - один проект
'''
def assign_role_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, j)
    w3 = []

    moon12 = moon()
    delta = delta_role_project_12(role, project)
    people = real_and_virtual_people(role)
    dem_rj = needs_role_project_12(person,role, project)  # ----------------

    for person in people:
        if person == None:
            break
        b_w3 = [0] * 12
        a_w3 = task_person_role_project_12(person, role, project)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        try:
            p = person.id
        except:
            p = 0
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"
            try:
                df = diff[i]
            except:
                df = 0
            b_w3[i] = {
                "link": f"{p}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i], 0), df),
                "val": a_w3[i],
                "color": color,
                "fire": df < 0,
            }
            d = inc(d)

        c_w3 = [{"val": person.fio}] + b_w3
        p100 = -1
        w3.append(c_w3)

    moon12["w3"] = w3

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["j"] = j
    return render(request, "ujr.html", moon12)
'''
назначения - один проект
'''
def assign_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w3 = []

    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        delta = delta_role_project_12(role, project)
        people = real_and_virtual_people(role)
        dem_rj = needs_role_project_12(person,role, project)  # ----------------
        
        p100 = {"val": role.title}
        for person in people:
            diff = rest_of_time_pr_12(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)

            d = date0()
            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "fire": diff[i] < 0,
                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

    moon12["w3"] = w3

    moon12["role"] = "Все ресурсы"

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = 0
    moon12["j"] = j
    return render(request, "uj.html", moon12)

'''
назначения - один ресурс
'''
def assign_role(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, -1)
    w3 = []

    moon12 = moon()

    people = real_and_virtual_people(role)
    projects = Project.objects.all()

    for project in projects:
        delta = delta_role_project_12(role, project)
        p100 = {"val": project.title}
        for person in people:
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)
            diff = rest_of_time_pr_12(person, role)
            d = date0()
            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"

                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "fire": diff[i] < 0,
                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

    moon12["w3"] = w3
    moon12["role"] = role
    moon12["project"] = project
    moon12["r"] = r

    return render(request, "ur.html", moon12)
'''
дельта - один ресурс - один проект
'''
def delta_role_project(request, p, r, j):
    person, role, project = get_prj_triplet(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    delta = delta_role_project_12(role, project)

    w4 = []

    people_rv = real_and_virtual_people(role)
    people_rr = real_people(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + rest_of_time_pr_12(person, role))

    a_w2 = [0] * 12
    dem_rj = needs_role_project_12(person,role, project)   # ----------------

    d = date0()
    for i in range(12):
        color = "white"
        if mon_outside_prj(d, project):
            color = "lightgrey"
        elif dem_rj[i] > 0:
            color = "lightblue"
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color": color,
        }  #

        d = inc(d)
    w2 = a_w2

    for person in people_rv:
        if person == None:
            break
        b_w3 = [0] * 12
        a_w3 = task_person_role_project_12(person, role, project)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"

            try:
                p = person.id
                df = diff[i]
            except:
                p = 0
                df = 0

            b_w3[i] = {
                "link": f"{p}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i], 0), df),
                "val": a_w3[i],
                "color": color,
            }
            d = inc(d)

        c_w3 = [{"val": person.fio}] + b_w3
        p100 = -1
        w3.append(c_w3)

    w1.append(delta)  ############################
    moon12["w1"] = w1
    moon12["w2"] = w2
    moon12["w3"] = w3
    moon12["w4"] = w4

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    moon12["p"] = 0
    return render(request, "djr.html", moon12)

'''
балансы - один ресурс - один проект
'''
def all_role_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    zo = ["АУТСОРС"] + outsrc(role, project)
    zv = ["ВАКАНСИЯ"] + vacancia(role, project)
    w4 = []

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + rest_of_time_pr_12(person, role))

    a_w2 = [0] * 12
    dem_rj = ["Потребность"] + needs_role_project_12(person,role, project)  # ----------------

    d = date0()
    for i in range(12):
        color = "white"
        if mon_outside_prj(d, project):
            color = "lightgrey"
        elif dem_rj[i + 1] > 0:
            color = "lightblue"
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i + 1],
            "color": color,
        }  #

        d = inc(d)
    w2 = a_w2

    supp = ["Поставка"] + task_role_project_12(role, project)
    delta = ["Дельта"] + delta_role_project_12(role, project)

    for person in people_rv:
        if person == None:
            break
        b_w3 = [0] * 12
        a_w3 = task_person_role_project_12(person, role, project)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
                if delta[i + 1] < 0:
                    color = "#B266FF"
            elif delta[i + 1] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"

            b_w3[i] = {
                "link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i + 1], 0), diff[i]),
                "val": a_w3[i],
                "color": color,
            }

            d = inc(d)

        c_w3 = [{"val": person.fio}] + b_w3
        p100 = -1
        w3.append(c_w3)

    w1.append(dem_rj)  ##########################################77777
    w1.append(supp)  ###############--
    w1.append(zo)  ################
    w1.append(zv)  #####################
    w1.append(delta)  ############################
    moon12["w1"] = w1
    moon12["w2"] = w2
    moon12["w3"] = w3
    moon12["w4"] = w4

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    moon12["p"] = 0
    return render(request, "ajr.html", moon12)

'''
балансы - один ресурс
'''
def all_role(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)
    w3 = []
    w2 = []
    w1 = []
    w4 = []
    moon12 = moon()
    projects = Project.objects.all()

    x = [0] * 12

    for person in people_rr:
        diff = rest_of_time_pr_12(person, role)
        x = diff
        w4.append([person.fio] + x)
    for project in projects:
        zo = ["АУТСОРС"] + outsrc(role, project)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project)

        p200 = project.title
        a_w2 = [{"val": project.title, "j": project.id, "r": r}] + [0] * 12
        dem_rj = [project.title] + ["Потребность"] + needs_role_project_12(person, role, project)  #

        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i + 2] > 0:
                color = "lightblue"
            a_w2[i + 1] = {
                "val": dem_rj[i + 2],
                "j": project.id,
                "r": role.id,
                "color": color,
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
            }
            d = inc(d)
        w2.append(a_w2)  # --------

        supp = ["Поставка"] + task_role_project_12(role, project)
        delta = ["Дельта"] + delta_role_project_12(role, project)

        p100 = project.title
        for person in people_rv:
            diff = rest_of_time_pr_12(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)
            d = date0()

            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i + 1] < 0:
                        color = "#B266FF"
                elif delta[i + 1] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"

                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i + 1], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                }
                ##########################################################################3333333
                d = inc(d)
            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        w1.append(dem_rj)  ##########################################77777
        w1.append([-1] + supp)  ###############--
        w1.append([-1] + zo)  ################

        w1.append([-1] + zv)  #####################
        w1.append([-1] + delta)  ############################

    moon12["w4"] = w4  ########################################
    moon12["w2"] = w2  #####################
    moon12["w1"] = w1  ###############################
    moon12["w3"] = w3

    moon12["project"] = "Все проекты"
    moon12["role"] = role
    moon12["r"] = r
    moon12["j"] = 0
    moon12["p"] = 0

    return render(request, "ar.html", moon12)
'''
дельта - один ресурс
'''
def delta_role(request, p, r, j):
    person, role, project = get_prj_triplet(-1, r, -1)

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)
    w3 = []
    w2 = []
    w1 = []
    w4 = []
    moon12 = moon()

    x = [0] * 12

    for person in people_rr:
        diff = rest_of_time_pr_12(person, role)
        x = diff
        w4.append([person.fio] + x)

    projects = Project.objects.all()

    # W222222222222222222222222222222
    for project in projects:
        p100 = project.title
        a_w2 = [
            {
                "val": project.title,
                "j": project.id,
                "r": role.id,
            }
        ] + [0] * 12

        dem_rj = [project.title] + ["Потребность"] + needs_role_project_12(person,role, project)   #

        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i + 2] > 0:
                color = "lightblue"
            a_w2[i + 1] = {
                "val": dem_rj[i + 2],
                "j": project.id,
                "r": role.id,
                "color": color,
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
            }
            d = inc(d)
        w2.append(a_w2)  # --------

        delta = delta_role_project_12(role, project)

        for person in people_rv:
            diff = rest_of_time_pr_12(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)

            d = date0()

            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"

                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                }
                ##########################################################################3333333
                d = inc(d)
            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        delta2 = [{"val": x} for x in delta]        
        w1.append([{"j": project.id, "val": project.title}] + delta2)  

    moon12["w4"] = w4  ########################################
    moon12["w2"] = w2  #####################
    moon12["w1"] = w1  ###############################
    moon12["w3"] = w3

    moon12["role"] = role
    moon12["r"] = r
    moon12["j"] = 0
    moon12["p"] = 0
    moon12["project"] = "Все проекты"

    return render(request, "dr.html", moon12)
'''

дельта - один проект
'''
def delta_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()


    roles = Role.objects.all()
    for role in roles:
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        p6 = role.title
        for person in people_rr:  # 7777777777777777777777777777777777777777
            diff = rest_of_time_pr_12(person, role)
            w4.append([p6, person.fio] + diff)
            p6 = -1

        delta = delta_role_project_12(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project_12(person,role, project)  # ----------------

        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i] > 0:
                color = "lightblue"

            a_w2[i] = {
                "val": dem_rj[i],
                "color": color,
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
            }

            d = inc(d)
        w2.append(
            [
                {
                    "r": role.id,
                    "j": project.id,
                    "val": role.title,
                    "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                }
            ]
            + a_w2
        )

        p100 = role.title
        for person in people_rv:
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)
            diff = rest_of_time_pr_12(person, role)
            d = date0()
            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"

                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        delta2 = [{"val": x} for x in delta]
        w1.append(
            [{"r": role.id, "val": role.title}] + delta2
        )  ############################
    moon12["w1"] = w1
    moon12["w2"] = w2
    moon12["w3"] = w3
    moon12["w4"] = w4

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["j"] = j

    moon12["r"] = 0

    moon12["p"] = 0
    return render(request, "dj.html", moon12)

'''
балансы - один проект
'''
def all_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    roles = Role.objects.all()
    a_w2 = [0] * 12
    for role in roles:
        zo = ["АУТСОРС"] + outsrc(role, project)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project)
        supp = ["Поставка"] + task_role_project_12(role, project)
        delta = ["Дельта"] + delta_role_project_12(role, project)
        dem_rj = needs_role_project_12(person,role, project)   # ----------------

        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i] > 0:
                color = "lightblue"

            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
            }  #
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

        p100 = role.title
        p200 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        for person in people_rr:  #
            diff = rest_of_time_pr_12(person, role)
            w4.append([p200, person.fio] + diff)
            p200 = -1
        for person in people_rv:  #
            diff = rest_of_time_pr_12(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project_12(person, role, project)

            d = date0()
            for i in range(12):
                color = "white"
                if mon_outside_prj(d, project):
                    color = "lightgrey"
                    if delta[i + 1] < 0:
                        color = "#B266FF"
                elif delta[i + 1] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"

                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i + 1], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        w1.append(
            [role.title, "Потребность"] + dem_rj
        )  ##########################################77777
        w1.append([-1] + supp)  ###############--
        w1.append([-1] + zo)  ################
        w1.append([-1] + zv)  #####################
        w1.append([-1] + delta)  ############################
    moon12["w1"] = w1
    moon12["w2"] = w2
    moon12["w3"] = w3
    moon12["w4"] = w4

    moon12["role"] = "Все ресурсы"

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = 0
    moon12["j"] = j

    moon12["p"] = 0
    return render(request, "aj.html", moon12)  # АЛьфа, один проект все ресурсы
'''
потребность - один ресурс - один проект
'''
def needs_role_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, j)
    if role == None:
        return home(request)
    w2 = []
    moon12 = moon()

    delta = delta_role_project_12(role, project)

    a_w2 = [0] * 12
    dem_rj = needs_role_project_12(person,role, project)   # ----------------

    d = date0()
    for i in range(12):
        color = "white"
        if mon_outside_prj(d, project):
            color = "lightgrey"
        elif dem_rj[i] > 0:
            color = "lightblue"
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color": color,
        }
        d = inc(d)
    w2.append([{"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = r
    moon12["id"] = j
    return render(request, "mmjr.html", moon12)

'''
потребность - прект один  -ресурсы все
'''
def needs_project(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, -1, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        delta = delta_role_project_12(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project_12(person,role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i] > 0:
                color = "lightblue"
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
            }
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = "Все ресурсы"

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = 0
    moon12["id"] = j
    return render(request, "mmj.html", moon12)

'''
потребность - ресурс один - проекты все
'''
def needs_role(request:object, p:int, r:int, j:int)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    w2 = []
    moon12 = moon()

    projects = Project.objects.all()
    for project in projects:
        delta = delta_role_project_12(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project_12(person,role, project)   # ----------------

        d = date0()
        for i in range(12):
            color = "white"
            if mon_outside_prj(d, project):
                color = "lightgrey"
            elif dem_rj[i] > 0:
                color = "lightblue"
            a_w2[i] = {
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
            }
            d = inc(d)
        w2.append([{"val": project.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = "Все проекты"
    moon12["j"] = j
    moon12["r"] = r
    moon12["id"] = j
    return render(request, "mmr.html", moon12)


''' 
доступность остаточная - персональная - один вид ресурса
'''
def rest_role(request:object, p:int, r:int, j:int)->object:
    moon12 = moon()
    dif14 = []
    dif15 = []
    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    people_rr = real_people(role)

    for person in people_rr:
        dif = time_available_person_role_12(person, role)

        dif100 = [0] * 12
        da = date0()
        for i in range(12):
            dif100[i] = {
                "link": f"{person.id}.0.0.{da.year}-{da.month}-15",
                "up": up(1, 2),
                "title": dif[i],
            }  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    for person in people_rr:
        dif = rest_of_time_pr_12(person, role)

        dif100 = [0] * 12
        da = date0()
        for i in range(12):
            dif100[i] = {
                "link": f"{person.id}.0.0.{da.year}-{da.month}-15",
                "title": dif[i],
            }  # 9898
            da = inc(da)
        dif15.append([person.fio] + dif100)  ######################

    moon12["dif14"] = dif14

    moon12["dif15"] = dif15
    moon12["r"] = r
    moon12["role"] = role

    return render(request, "mr2.html", moon12)

'''
доступность максимальная - персональная - один вид ресурса
'''
def available_role(request:object, p:int, r:int, j:int)->object:
    moon12 = moon()
    dif14 = []
    dif15 = []

    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)

    for person in people_rr:
        dif = time_available_person_role_12(person, role)
        is100 = person_more_100_12(person)

        dif100 = [0] * 12
        da = date0()
        for i in range(12):
            dif100[i] = {
                "link": f"{person.id}.{r}.0.{da.year}-{da.month}-15",
                "fire": is100[i],
                "val": dif[i],
            }  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    moon12["dif14"] = dif14

    moon12["dif15"] = dif15
    moon12["r"] = r
    moon12["role"] = role

    return render(request, "mr1.html", moon12)


'''
показать максимальную доступность по всем персонам и ролям
'''
def available_all(request:object)->object:  # Максимальная доступнасть по всем ресурсам
    moon12 = moon()
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()

    my = UserProfile.objects.all()
    arr = [0] * 100
    for p in my:
        arr[p.id] = [0] * 1000
        for r in roles:
            t = time_available_person_role_12(p, r)
            arr[p.id][r.id] = [0] * 12
            for i in range(12):
                arr[p.id][r.id][i] += t[i]

    for role in roles:
        p9 = role.title
        people_rr = real_people(role)

        px = {"val": role.title, "r": role.id}  #######################
        for person in people_rr:
            is100 = person_more_100_12(person)

            dif2 = [{"val": person.fio}] + [0] * 12
            dif = [person.fio] + time_available_person_role_12(person, role)
            d = date0()
            for i in range(12):
                if arr[person.id][role.id][i] > 100:
                    color = "pink"
                else:
                    color = "white"

                dif2[i + 1] = {
                    "link": f"{person.id}.{role.id}.0.{d.year}-{d.month}-15",
                    "color": color,
                    "val": dif[i + 1],
                    "fire": is100[i],
                }
                d = inc(d)

            dif14.append([px] + dif2)  ######################
            px = -1  ##################################

    moon12["dif14"] = dif14  ########################################

    return render(request, "mrom.html", moon12)


'''
показать остаток ресурса по всем персонам и ролям
'''
def rest_all(request:object)->object:  # Остаточная доступость по всем ресурсам
    moon12 = moon()
    dif14 = []

    project = None #Project.objects.all()
    roles = Role.objects.all()
    for role in roles:
        p9 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        px = role.title
        for person in people_rr:
            dif = [person.fio] + rest_of_time_pr_12(person, role)
            dif14.append([px] + dif)
            px = -1

    moon12["dif14"] = dif14

    return render(request, "mro.html", moon12)


'''
портфель проектов
'''

def table_timeline(request:object)->object:  # все проекты (портфель)
    moon12 = moon()
    projects = Project.objects.all().order_by("general", "start_date")
    data = []
    for p in projects:
        data.append(project_timeline_line(p))
    moon12["matrix"] = data
    return render(request, "prjlist.html", moon12)


import babel.dates
from datetime import date
'''
одна строка в портфель проектов
'''
import babel
def project_timeline_line(p):

    dmin = date.today()
    dmin = dmin.replace(day=15)
    dmax = inc_n(dmin, 11)    
    L = []
    L.append(p.general.fio)
    L.append({"title": p.title, "id": p.id})  # 989898

    formatted_date = babel.dates.format_date(p.start_date, "d MMM YY", locale='ru')
    L.append( formatted_date)

    formatted_date = babel.dates.format_date(p.end_date, "d MMM YY", locale='ru')
    L.append( formatted_date)


    L+=[dif(p.start_date, p.end_date)] + mon_bool(dmin, dmax, p.start_date, p.end_date)

    return L

