from .models import Less
from .forms import EntryForm, ProjectForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .utils import *
from .db import *
from typing import List, Union,Dict,Callable


'''
Объект Вакансия - загрузка на год
'''
def vacancia(role:object, project:object)->List[int]:
    person = None
    try:
        person = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]  ##АУТСОРС
    except:
        pass
    return task_person_role_project(person, role, project)

'''
Объект Аутсорс - загрузка на год
'''
def outsrc(role:object, project:object)->List[int]:
    person = None
    try:
        person = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        pass
    return task_person_role_project(person, role, project)





def b(request, n):
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
            x = round(100 * dell(role, project, n) / demm(role, project, n))

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





def atest(request):
    a = outsrc(2, 2)
    b = vacancia(2, 2)

    return render(request, "a_test.html", {"a": a, "b": b})


'''
домашняя страница
'''
def home(request):
    return render(request, "x_home.html", {})


from django.shortcuts import render, get_object_or_404, redirect


def alff(request, id=None):
    instance = None
    if id:
        instance = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("prjlist")

    else:
        form = ProjectForm(instance=instance)
    return render(request, "form.html", {"form": form})



def atj(request):
    projects = Project.objects.all().order_by("general")
    data = []
    for p in projects:
        x = {"j": p.id, "project": p.title, "name": p.general.fio}
        data.append(x)
    context = {"data": data}

    return render(request, "atj.html", context)


def atr(request):
    context = {}
    roles = Role.objects.all().order_by("general")
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {"title": p.title, "r": p.id, "name": u.fio}
        data2.append(x)
    context["data2"] = data2

    return render(request, "atr.html", context)


def a00(request):
    return render(request, "a00.html")


def diffx(person, role):
    return pr_dif_(person, role)

'''
Заголовок - 12 месяцев
'''
def moon()->List[object]:
    y_data = []
    m_data = []
    ym = []
    d = date.today().replace(day=15)
    for i in range(12):
        y_data.append(d.year)
        m_data.append(d.month)
        ym.append({"y": d.year, "m": d.month})
        d = inc(d)
    return {"yy": y_data, "mm": m_data, "ym": ym}
    ##################################################################


def ujr(request, p, r, j):
    person, role, project = get_prj_triplet(-1, r, j)
    w3 = []

    moon12 = moon()
    delta = delta_role_project(role, project)

    people = real_and_virtual_people(role)
    dem_rj = needs_role_project(role, project)  # ----------------

    for person in people:
        if person == None:
            break
        b_w3 = [0] * 12
        a_w3 = task_person_role_project(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
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
    moon12["r"] = r
    moon12["j"] = j
    return render(request, "ujr.html", moon12)


def uj(request, p, r, j):
    person, role, project = get_prj_triplet(-1, -1, j)
    w3 = []

    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        delta = delta_role_project(role, project)

        people = real_and_virtual_people(role)
        dem_rj = needs_role_project(role, project)  # ----------------
        p100 = {"val": role.title}
        for person in people:
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project(person, role, project)

            d = date.today().replace(day=15)
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


def ur(request, p, r, j):
    person, role, project = get_prj_triplet(-1, r, -1)
    w3 = []

    moon12 = moon()

    people = real_and_virtual_people(role)
    projects = Project.objects.all()

    for project in projects:
        delta = delta_role_project(role, project)
        p100 = {"val": project.title}
        for person in people:
            b_w3 = [0] * 12
            a_w3 = task_person_role_project(person, role, project)
            diff = pr_dif_(person, role)
            d = date.today().replace(day=15)
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


def djr(request, p, r, j):
    person, role, project = get_prj_triplet(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    delta = delta_role_project(role, project)

    w4 = []

    people_rv = real_and_virtual_people(role)
    people_rr = real_people(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + pr_dif_(person, role))

    a_w2 = [0] * 12
    dem_rj = needs_role_project(role, project)  # ----------------

    d = date.today().replace(day=15)
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
        a_w3 = task_person_role_project(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
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


# Дельта, один проект, один ресурс
def ajr(request, p, r, j):  # Альфа, один проект, один ресуря
    person, role, project = get_prj_triplet(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    supp = [-1, "Поставка"] + task_role_project(role, project)
    delta = ["Дельта"] + delta_role_project(role, project)
    zo = ["АУТСОРС"] + outsrc(role, project)
    zv = ["ВАКАНСИЯ"] + vacancia(role, project)
    w4 = []

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + pr_dif_(person, role))

    a_w2 = [0] * 12
    dem_rj = ["Потребность"] + needs_role_project(role, project)  # ----------------

    d = date.today().replace(day=15)
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

    supp = ["Поставка"] + task_role_project(role, project)
    delta = ["Дельта"] + delta_role_project(role, project)

    for person in people_rv:
        if person == None:
            break
        b_w3 = [0] * 12
        a_w3 = task_person_role_project(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
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


def ar(request, p, r, j):
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
        diff = pr_dif_(person, role)
        x = diff
        w4.append([person.fio] + x)
    for project in projects:
        zo = ["АУТСОРС"] + outsrc(role, project)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project)

        p200 = project.title
        a_w2 = [{"val": project.title, "j": project.id, "r": r}] + [0] * 12
        dem_rj = [project.title] + ["Потребность"] + needs_role_project(role, project)  #

        d = date.today().replace(day=15)
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

        supp = ["Поставка"] + task_role_project(role, project)
        delta = ["Дельта"] + delta_role_project(role, project)

        p100 = project.title
        for person in people_rv:
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project(person, role, project)
            d = date.today().replace(day=15)

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


def dr(request, p, r, j):
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
        diff = pr_dif_(person, role)
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

        dem_rj = [project.title] + ["Потребность"] + needs_role_project(role, project)  #

        d = date.today().replace(day=15)
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

        delta = delta_role_project(role, project)

        for person in people_rv:
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project(person, role, project)

            d = date.today().replace(day=15)

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
        # w1.append([project.title]+delta)############################
        w1.append(
            [{"j": project.id, "val": project.title}] + delta2
        )  ############################

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


def dj(request, p, r, j):  # Дельта, один проект все ресурсы
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    w4 = []

    roles = Role.objects.all()
    for role in roles:
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        p6 = role.title
        for person in people_rr:  # 7777777777777777777777777777777777777777
            diff = pr_dif_(person, role)
            w4.append([p6, person.fio] + diff)
            p6 = -1

        delta = delta_role_project(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project(role, project)  # ----------------

        d = date.today().replace(day=15)
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
            a_w3 = task_person_role_project(person, role, project)
            diff = pr_dif_(person, role)
            d = date.today().replace(day=15)
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


def aj(request, p, r, j):  # Альфа, один проект
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    w4 = []

    roles = Role.objects.all()
    a_w2 = [0] * 12
    for role in roles:
        zo = ["АУТСОРС"] + outsrc(role, project)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project)
        supp = ["Поставка"] + task_role_project(role, project)
        delta = ["Дельта"] + delta_role_project(role, project)
        dem_rj = needs_role_project(role, project)  # ----------------

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
            }  #
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

        p100 = role.title
        p200 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        for person in people_rr:  #
            diff = pr_dif_(person, role)
            w4.append([p200, person.fio] + diff)
            p200 = -1
        for person in people_rv:  #
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = task_person_role_project(person, role, project)

            d = date.today().replace(day=15)
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


def mmjr(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj_triplet(-1, r, j)
    if role == None:
        return alf(request)
    w2 = []
    moon12 = moon()

    delta = delta_role_project(role, project)

    a_w2 = [0] * 12
    dem_rj = needs_role_project(role, project)  # ----------------

    d = date.today().replace(day=15)
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


def mmj(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj_triplet(-1, -1, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        delta = delta_role_project(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project(role, project)  # ----------------

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


def mmr(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj_triplet(-1, r, -1)

    w2 = []
    moon12 = moon()

    projects = Project.objects.all()
    for project in projects:
        delta = delta_role_project(role, project)

        a_w2 = [0] * 12
        dem_rj = needs_role_project(role, project)  # ----------------

        d = date.today().replace(day=15)
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




def mr2(
    request, p, r, j
):  # максимальна доступность одного ресурса и Остаточная доступность
    moon12 = moon()
    dif14 = []
    dif15 = []
    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    people_rr = real_people(role)

    for person in people_rr:
        dif = pr_isfree_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {
                "link": f"{person.id}.0.0.{da.year}-{da.month}-15",
                "up": up(1, 2),
                "title": dif[i],
            }  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    for person in people_rr:
        dif = pr_dif_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
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


def mr1(
    request, p, r, j
):  # максимальна доступность одного ресурса и Остаточная доступность
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
        dif = pr_isfree_(person, role)
        is100 = person_more_100(person)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
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


#
def mrom(request):  # Максимальная доступнасть по всем ресурсам
    moon12 = moon()
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()

    my = UserProfile.objects.all()
    arr = [0] * 100
    for p in my:
        arr[p.id] = [0] * 1000
        for r in roles:
            t = pr_isfree_(p, r)
            arr[p.id][r.id] = [0] * 12
            for i in range(12):
                arr[p.id][r.id][i] += t[i]

    for role in roles:
        p9 = role.title
        people_rr = real_people(role)

        px = {"val": role.title, "r": role.id}  #######################
        for person in people_rr:
            is100 = person_more_100(person)

            dif2 = [{"val": person.fio}] + [0] * 12
            dif = [person.fio] + pr_isfree_(person, role)
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


#
def mro(request):  # Остаточная доступость по всем ресурсам
    moon12 = moon()
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()
    for role in roles:
        p9 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        px = role.title
        for person in people_rr:
            dif = [person.fio] + diffx(person, role)
            dif14.append([px] + dif)
            px = -1

    moon12["dif14"] = dif14

    return render(request, "mro.html", moon12)



def project_timeline(request:object)->any:  # все проекты (портфель)
    
    moon12 = moon()
    projects = Project.objects.all().order_by("general", "start_date")
    data = []
    for p in projects:
        data.append(project_timeline_line(p))
    moon12["matrix"] = data
    return render(request, "prjlist.html", moon12)

def project_timeline_line(p):
    dmin = date.today()
    dmin = dmin.replace(day=15)
    dmax = inc_n(dmin, 11)    
    L = []
    L.append(p.general.fio)
    L.append({"title": p.title, "id": p.id})  # 989898
    L.append(p.start_date)
    L.append(p.end_date)
    L+=[dif(p.start_date, p.end_date)] + mon_bool(dmin, dmax, p.start_date, p.end_date)

    return L

'''
Загрузка одно человека по разным ролям суммарно превысила 100% (булев вектор)
'''
def person_more_100(person:object)->List[bool]:
    sum = [0] * 12
    roles = {person.role}.union(person.res.all())
    for role in roles:
        isfree = pr_isfree_(person, role)
        for i in range(12):
            sum[i] += isfree[i]
    res = [True] * 12
    for i in range(12):
        res[i] = sum[i] > 100
    return res