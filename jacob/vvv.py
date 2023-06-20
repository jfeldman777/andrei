from typing import List

from django.shortcuts import redirect, get_object_or_404

from .db import delta_role_project_12, needs_role_project_12, person_more_100_12, task_role_project_12
from .db import get_prj_triplet, rest_of_time_pr_12, time_available_person_role_12
from .db import task_person_role_project_12, real_and_virtual_people, real_people, rest_and_color_12
from .utils import *
from datetime import date
from .models import UserProfile, Grade, Wish,Project
from .view_forms import role_form
from django.urls import resolve
from .paint import Paint

'''
отсюда можно запускать тесты
'''
def atest(request:object)->object:
    return render(request, "a00.html")

def atest1(request:object)->object:
    return render(request, "a001.html")
# def atest2(request:object)->object:
#     return role_form(request,id=None, file_name="a002.html")

'''
домашняя страница
'''
def home(request):
    return render(request, "x_home.html", {})


'''
Объект Вакансия - загрузка на год
'''
def vacancia(role:object, project:object,n:int=12)->List[int]:
    person = None
    person = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]  ##АУТСОРС
    return task_person_role_project_12(person, role, project,n)

'''
Объект Аутсорс - загрузка на год
'''
def outsrc(role:object, project:object,n:int=12)->List[int]:
    person = None
    try:
        person = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        pass
    return task_person_role_project_12(person, role, project,n)




def delta_on_span(r, j, n):
    rjd = delta_role_project_12(r, j,n)
    s = -sum(filter(lambda x: x < 0, rjd))
    return s

'''
НЕехватка ресурсов - роль - проект - время-месяцев - суммарно по месяцам
'''
def needs_on_span(r:object, j:object, n:int)->int:
    rjd = needs_role_project_12(-1,r, j,n)
    s = sum(rjd)
    if s == 0:
        return 1 #чтобы не делить на ноль
    return s

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
        txy[j] = {"val": roles[j].title, "link": f"/delta_r/0/{roles[j].id}/0/"}

    paint = Paint()
    for i in range(len(projects)):
        paint.next_row(projects[i])
        xy[i][0] = {"color": paint.rgb_back(),
            "val": projects[i], "link": f"/delta_j/0/0/{projects[i].id}/"}

        for j in range(len(roles)):


            project = projects[i]
            role = roles[j]
            x = round(100 * delta_on_span(role, project, n) / needs_on_span(role, project, n))
            paint.next_cell(x)


            xy[i][j + 1] = {
                "val": f"{x}%",
                "link": f"/delta_jr/0/{roles[j].id}/{projects[i].id}/",
                "color": paint.color_entry_map(),
                "i": project.id,
                "j": role.id,
            }
    context = {"tab": xy, "txy": txy, "n": n, "hh": n2txt(n)}

    return render(request, "b.html", context)

'''
Все проекты в одной таблице

'''

def table_projects(request:object)->object:
    paint = Paint()
    projects = Project.objects.all().order_by("general")
    data = []
    for i in range(len(projects)):
        paint.next_row(None)
        p = projects[i]
        data.append({"j": p.id, "project": p.title, "name": p.general.fio,
             "color2":paint.rgb_back_right(),
             "color1":paint.rgb_back_left()
             })


    context = {"data": data}
    return render(request, "tab_j.html", context)

'''
Все ресурсы в одной таблице
'''
def table_resources(request:object)->object:
    paint = Paint()
    context = {}
    data = []
    roles = Role.objects.all().order_by("general")
    for i in range(len(roles)):
        paint.next_row(None)
        p = roles[i]
        data.append({"title": p.title, "r": p.id,
                      "color2": paint.rgb_back_right(),
                      "color1": paint.rgb_back_left(),
                      "name":UserProfile.objects.get(user=p.general).fio})

    context["data2"] = data
    return render(request, "tab_r.html", context)


def people(request):
    paint = Paint()
    context = {}
    profiles = UserProfile.objects.filter(virtual=False).order_by("fio")
    nx = len(Role.objects.all())
    data2 = []
    npLmax = 2
    for profile in profiles:
        paint.next_row(None)
        try:
            grade1 = Grade.objects.filter(person=profile,role=profile.role).first().mygrade
        except:
            grade1 = '0'
        profile_data = {"fio": profile.fio, "role": profile.role,
                        "grade":grade1,
                        "color":paint.rgb_back_left(),
                        "res": [], "id": profile.id}
        pL = profile.res.all()
        for role in pL:
            if role != profile.role:
                grade = Grade.objects.filter(person=profile,role=role).first()
                grade_value = grade.mygrade if grade else '0'

                profile_data["res"].append({"role": str(role), "grade": grade_value,
                                            "color": paint.rgb_back_right(),
                                            "id":role.id})


        data2.append(profile_data)
    context["data2"] = data2



    return render(request, "people.html", context)
def roles(request:object)->object:
    context = {}
    roles = Role.objects.all().order_by("general")
    data2 = [{"title": p.title, "id": p.id, "general": p.general.userprofile.fio}
                        for p in roles]
    context["data2"] = data2

    return render(request, "roles.html", context)
'''
Заголовок - 12 месяцев
'''
def moon(n:int=12)->List[object]:
    L = ['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек',]
    ym = []
    d = date0()
    for i in range(n):
         ym.append({"y": str(d.year)[2:],"m": L[d.month-1]})
         d = inc(d)
    return  { "ym": ym}

def moon4(n: int = 12) -> List[object]:
        ym = []
        d = date0()
        for i in range(n):
            ym.append({"y": d.year, "m": d.month})
            d = inc(d)
        return {"ym": ym}

    ##################################################################

'''
назначения - один ресурс - один проект
'''
def task_role_project(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, j)
    try:
        wish = Wish.objects.get(role=role, project=project, ).mywish
    except:
        wish = ''
    w3 = []

    moon12 = moon()
    delta = delta_role_project_12(role, project,n)
    people = real_and_virtual_people(role)
    dem_rj = needs_role_project_12(person,role, project,n)  # ----------------

    for person in people:
        if person == None:
            break
        b_w3 = [0] * n
        a_w3 = task_person_role_project_12(person, role, project,n)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        try:
            p = person.id
        except:
            p = 0
        for i in range(n):
            tclass = ""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"
            else:
                tclass="color"


            try:
                df = diff[i]
            except:
                df = 0
            b_w3[i] = {
                "link": f"{p}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i], 0), df,wish),
                "val": a_w3[i],
                "color": color,
                "fire": df < 0,
                "class":tclass + "  good"
            }
            d = inc(d)
        up1 = ''
        if not person.virtual:
            try:
                grade = Grade.objects.get(person=person, role=role).mygrade
            except:
                grade = '0'
            up1=f" ({grade})"
        c_w3 = [{"val": person.fio + up1}] + b_w3

        w3.append(c_w3)

    moon12["w3"] = w3
    moon12["role"] = role
    moon12["r"] = r
    moon12["project"] = project
    moon12["id"] = j
    moon12["j"] = j
    return render(request, "tasks_jr.html", moon12)
'''
назначения - один проект
'''
def task_project(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w3 = []

    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        try:
            wish = Wish.objects.get(role=role,project=project,).mywish
        except:
            wish=''
        delta = delta_role_project_12(role, project,n)
        people = real_and_virtual_people(role)
        dem_rj = needs_role_project_12(person,role, project,n)  # ----------------
        
        p100 = {"val": role.title}
        for person in people:
            diff = rest_of_time_pr_12(person, role,n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)

            d = date0()
            for i in range(n):
                tclass=""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color = "rgb(211,211,211)"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass = "color"
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i],wish),
                    "val": a_w3[i],
                    "color": color,
                    "fire": diff[i] < 0,
                    'class':tclass + "  good"
                }
                d = inc(d)

            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1=f" ({grade})"
            c_w3 = [p100,{"val": person.fio + up1}] + b_w3
   
            w3.append(c_w3)

    moon12["w3"] = w3
    moon12["role"] = "Все ресурсы"
    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    return render(request, "tasks_j.html", moon12)

'''
назначения - один ресурс
'''
def task_role(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    w3 = []
    moon12 = moon()
    people = real_and_virtual_people(role)
    projects = Project.objects.all()

    for project in projects:
        try:
            wish = Wish.objects.get(role=role,project=project,).mywish
        except:
            wish=''
        delta = delta_role_project_12(role, project,n)
        p100 = {"val": project.title}
        for person in people:
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)
            diff = rest_of_time_pr_12(person, role,n)
            d = date0()
            for i in range(n):
                tclass=""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color = "rgb(211,211,211)"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass = "color"
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i],wish),
                    "val": a_w3[i],
                    "color": color,
                    "fire": diff[i] < 0,
                    "class":tclass
                }
                d = inc(d)

            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1=f" ({grade})"
            c_w3 = [p100,{"val": person.fio + up1}] + b_w3
            w3.append(c_w3)

    moon12["w3"] = w3
    moon12["role"] = role
    moon12["project"] = project
    moon12["r"] = r
    moon12["j"] = j
    return render(request, "tasks_r.html", moon12)
'''
дельта - один ресурс - один проект
'''
def delta_role_project(request, p, r, j,n=12):
    person, role, project = get_prj_triplet(-1, r, j)
    try:
        wish = Wish.objects.get(role=role, project=project, ).mywish
    except:
        wish = ''

    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    delta = delta_role_project_12(role, project,n)

    w4 = []

    people_rv = real_and_virtual_people(role)
    people_rr = real_people(role)
    paint4 = Paint()
    for person in people_rr:
        paint4.next_row(None)
        dif = [{"color":paint4.rgb_back_left(),
                "val":person.fio}] + rest_and_color_12(person, role,paint4.color_rest,12)
        w4.append(dif)






    a_w2 = [0] * n
    dem_rj = needs_role_project_12(person,role, project,n)   # ----------------

    d = date0()
    tcolor=""
    for i in range(n):
        tcolor = ""
        color = "rgb(240,240,240)"
        if mon_outside_prj(d, project):
            color = " rgb(211,211,211) "
        elif dem_rj[i] > 0:
            color = "lightblue"
        else:
            tcolor="color"
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color": color,
            "class":tcolor + "  good"
        }  #

        d = inc(d)
    w2 = a_w2

    for person in people_rv:
        if person == None:
            break
        b_w3 = [0] * n
        a_w3 = task_person_role_project_12(person, role, project,n)
        diff = rest_of_time_pr_12(person, role,n)
        d = date0()
        for i in range(n):
            tcolor=""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"
            else:
                tcolor="color"

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
                "class":tcolor+" good ",
            }
            d = inc(d)

        up1 = ''
        if not person.virtual:
            try:
                grade = Grade.objects.get(person=person, role=role).mygrade
            except:
                grade = '0'
            up1=f" ({grade})"
        c_w3 = [{"class":"color","val": person.fio + up1}] + b_w3
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
    return render(request, "delta_jr.html", moon12)

'''
балансы - один ресурс - один проект
'''
def balance_role_project(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, j)
    try:
        wish = Wish.objects.get(role=role, project=project, ).mywish
    except:
        wish = ''
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
    paint4 = Paint()
    for person in people_rr:
        paint4.next_row(None)
        dif = [{"color":paint4.rgb_back_left(),
                "val":person.fio}] + rest_and_color_12(person, role,paint4.color_rest,12)
        w4.append(dif)


    a_w2 = [0] * n
    dem_rj = ["Потребность"] + needs_role_project_12(person,role, project,n)  # ----------------

    d = date0()
    for i in range(n):
        tclass= ""
        color = "rgb(240,240,240)"
        if mon_outside_prj(d, project):
            color = "rgb(211,211,211)"
        elif dem_rj[i + 1] > 0:
            color = "lightblue"
        else:
            tclass=" good color "
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i + 1],
            "color": color,
            "class":tclass
        }  #

        d = inc(d)
    w2 = a_w2

    supp = ["Поставка"] + task_role_project_12(role, project,n)
    delta = ["Дельта"] + delta_role_project_12(role, project,n)

    for person in people_rv:
        if person == None:
            break
        b_w3 = [0] * n
        a_w3 = task_person_role_project_12(person, role, project)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        for i in range(n):
            tclass=""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
                if delta[i + 1] < 0:
                    color = "#B266FF"
            elif delta[i + 1] < 0:
                color = "pink"
            elif a_w3[i] > 0:
                color = "lightblue"
            else:
                tclass=" color"

            b_w3[i] = {
                "link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i + 1], 0), diff[i]),
                "val": a_w3[i],
                "color": color,
                "class":tclass + "  good "
            }

            d = inc(d)
        up1 = ''
        if not person.virtual:
            try:
                grade = Grade.objects.get(person=person, role=role).mygrade
            except:
                grade = '0'
            up1=f" ({grade})"
        c_w3 = [{"class":"color","val": person.fio + up1}] + b_w3
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
    return render(request, "balance_jr.html", moon12)

'''
балансы - один ресурс
'''
def balance_role(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)
    w3 = []
    w2 = []
    w1 = []
    w4 = []
    moon12 = moon()
    projects = Project.objects.all()

    x = [0] * n

    paint4 = Paint()
    for person in people_rr:
        paint4.next_row(None)
        dif = [{"color": paint4.rgb_back_left(),
                "val": person.fio}] + rest_and_color_12(person, role, paint4.color_rest, 12)
        w4.append(dif)





    for project in projects:
        try:
            wish = Wish.objects.get(role=role, project=project, ).mywish
        except:
            wish = ''
        zo = ["АУТСОРС"] + outsrc(role, project)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project)

        p200 = project.title
        a_w2 = [{"class":"color",
            "val": project.title, "j": project.id, "r": r}] + [0] * n
        dem_rj = [project.title] + ["Потребность"] + needs_role_project_12(person, role, project,n)  #

        d = date0()
        for i in range(n):
            tclass = ""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i + 2] > 0:
                color = "lightblue"
            else:
                tclass="color"
            a_w2[i + 1] = {
                "val": dem_rj[i + 2],
                "j": project.id,
                "r": role.id,
                "color": color,
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "class": tclass + "  good"
            }
            d = inc(d)
        w2.append(a_w2)  # --------

        supp = ["Поставка"] + task_role_project_12(role, project,n)
        delta = ["Дельта"] + delta_role_project_12(role, project,n)

        p100 = project.title
        for person in people_rv:
            diff = rest_of_time_pr_12(person, role,n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)
            d = date0()

            for i in range(n):
                tclass = ""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color = "rgb(211,211,211)"
                    if delta[i + 1] < 0:
                        color = "#B266FF"
                elif delta[i + 1] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass = 'color'
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i + 1], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "class":tclass+ "  good"
                }
                ##########################################################################3333333
                d = inc(d)
            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100,{"class":"color","val": person.fio + up1}] + b_w3
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

    return render(request, "balance_r.html", moon12)
'''
дельта - один ресурс
'''
def delta_role(request, p, r, j,n=12):
    person, role, project = get_prj_triplet(-1, r, -1)

    people_rr = real_people(role)
    people_rv = real_and_virtual_people(role)
    w3 = []
    w2 = []
    w1 = []
    w4 = []
    moon12 = moon()

    x = [0] * n

    paint4 = Paint()
    for person in people_rr:
        paint4.next_row(None)
        dif = [{"color":paint4.rgb_back_left(),
                "val":person.fio}] + rest_and_color_12(person, role,paint4.color_rest,12)
        w4.append(dif)


    projects = Project.objects.all()

    # W222222222222222222222222222222
    for project in projects:
        try:
            wish = Wish.objects.get(role=role, project=project, ).mywish
        except:
            wish = ''
        p100 = project.title
        a_w2 = [
            {
                "val": project.title,
                "j": project.id,
                "r": role.id,
                "class": "color"
            }
        ] + [0] * n

        dem_rj = [project.title] + ["Потребность"] + needs_role_project_12(person,role, project,n)   #

        d = date0()
        for i in range(n):
            tclass=""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i + 2] > 0:
                color = "lightblue"
            else:
                tclass='color'
            a_w2[i + 1] = {
                "val": dem_rj[i + 2],
                "j": project.id,
                "r": role.id,
                "color": color,
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "class": tclass + "  good"
            }
            d = inc(d)
        w2.append(a_w2)  # --------

        delta = delta_role_project_12(role, project,n)

        for person in people_rv:
            diff = rest_of_time_pr_12(person, role,n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)

            d = date0()

            for i in range(n):
                tclass=""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color =  "rgb(211,211,211)"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass="color"

                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "class": tclass + "  good"
                }
                ##########################################################################3333333
                d = inc(d)
            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100,{"class":"color","val": person.fio + up1}] + b_w3
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

    return render(request, "delta_r.html", moon12)
'''

дельта - один проект
'''
def delta_project(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()


    roles = Role.objects.all()
    for role in roles:
        try:
            wish = Wish.objects.get(role=role, project=project, ).mywish
        except:
            wish = ''
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        p6 = role.title
        paint4 = Paint()
        for person in people_rr:
            paint4.next_row(None)
            dif = [{"color": paint4.rgb_back_left(),
                    "val": person.fio}] + rest_and_color_12(person, role, paint4.color_rest, 12)
            w4.append([p6] + dif)
            p6 = -1

        delta = delta_role_project_12(role, project)

        a_w2 = [0] * n
        dem_rj = needs_role_project_12(person,role, project,n)  # ----------------

        d = date0()
        for i in range(n):
            tclass=""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i] > 0:
                color = "lightblue"
            else:
                tclass='color'
            a_w2[i] = {
                "val": dem_rj[i],
                "color": color,
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "class":tclass+ "  good"
            }

            d = inc(d)
        w2.append(
            [
                {
                    "r": role.id,
                    "j": project.id,
                    "val": role.title,
                    "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                    "class":"color"
                }
            ]
            + a_w2
        )

        p100 = role.title
        for person in people_rv:
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)
            diff = rest_of_time_pr_12(person, role,n)
            d = date0()
            for i in range(n):
                tclass=""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color = "rgb(211,211,211)"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass="color"

                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "class":tclass+ "  good"
                }
                d = inc(d)

            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100,{"class":"color","val": person.fio + up1}] + b_w3
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
    return render(request, "delta_j.html", moon12)

'''
балансы - один проект
'''
def balance_project(request:object, p:int, r:int, j:int, n:int=12)->object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    roles = Role.objects.all()
    a_w2 = [0] * n
    for role in roles:
        zo = ["АУТСОРС"] + outsrc(role, project,n)
        zv = ["ВАКАНСИЯ"] + vacancia(role, project,n)
        supp = ["Поставка"] + task_role_project_12(role, project,n)
        delta = ["Дельта"] + delta_role_project_12(role, project,n)
        dem_rj = needs_role_project_12(person,role, project,n)   # ----------------

        d = date0()
        for i in range(n):
            tclass=""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i] > 0:
                color = "lightblue"
            else:
                tclass='color'
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
                "class": tclass + "  good"
            }  #
            d = inc(d)
        w2.append([{"class":"color","val": role.title}] + a_w2)

        p100 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)

        p6 = role.title
        paint4 = Paint()
        for person in people_rr:
            paint4.next_row(None)
            dif = [{"color": paint4.rgb_back_left(),
                    "val": person.fio}] + rest_and_color_12(person, role, paint4.color_rest, 12)
            w4.append([p6] + dif)
            p6 = -1


        for person in people_rv:  #
            diff = rest_of_time_pr_12(person, role,n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)

            d = date0()
            for i in range(n):
                tclass=""
                color = "rgb(240,240,240)"
                if mon_outside_prj(d, project):
                    color =  "rgb(211,211,211)"
                    if delta[i + 1] < 0:
                        color = "#B266FF"
                elif delta[i + 1] < 0:
                    color = "pink"
                elif a_w3[i] > 0:
                    color = "lightblue"
                else:
                    tclass="color"
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i + 1], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color,
                    "class": tclass + "  good"
                }
                d = inc(d)

            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1=f" ({grade})"
            c_w3 = [p100,{"class":"color","val": person.fio + up1}] + b_w3
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
    return render(request, "balance_j.html", moon12)  # АЛьфа, один проект все ресурсы
'''
потребность - один ресурс - один проект
'''
def needs_role_project(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, j)
    try:
        wish = Wish.objects.get(role=role, project=project, ).mywish
    except:
        wish = ''
    if role == None:
        return home(request)
    w2 = []
    moon12 = moon()

    delta = delta_role_project_12(role, project)

    a_w2 = [0] * n
    dem_rj = needs_role_project_12(person,role, project,n)   # ----------------

    d = date0()
    for i in range(n):
        tclass = ""
        color = "rgb(240,240,240)"
        if mon_outside_prj(d, project):
            color = "rgb(211,211,211)"
        elif dem_rj[i] > 0:
            color = "lightblue"
        else:
            tclass = "color"
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color": color,
            "class": tclass + "  good",
            'up':up(c=wish)
        }
        d = inc(d)
    w2.append(a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = r
    moon12["id"] = j
    return render(request, "needs_jr.html", moon12)

'''
потребность - прект один  -ресурсы все
'''
def needs_project(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, -1, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        try:
            wish = Wish.objects.get(role=role,project=project,).mywish
        except:
            wish=''
        delta = delta_role_project_12(role, project)

        a_w2 = [0] * n
        dem_rj = needs_role_project_12(person,role, project,n)  # ----------------

        d = date.today().replace(day=15)
        for i in range(n):
            tclass = ""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i] > 0:
                color = "lightblue"
            else :
                tclass="color"
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
                "class":tclass+ "  good",
                'up':up(c=wish)
            }
            d = inc(d)
        w2.append([{"class":"color",'up':up(c=wish),"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = "Все ресурсы"

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = 0
    moon12["id"] = j
    return render(request, "needs_j.html", moon12)

'''
потребность - ресурс один - проекты все
'''
def needs_role(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    w2 = []
    moon12 = moon()

    projects = Project.objects.all()
    for project in projects:
        try:
            wish = Wish.objects.get(project=project,role=role)
        except:
            wish = None

        delta = delta_role_project_12(role, project,n)

        a_w2 = [0] * n
        dem_rj = needs_role_project_12(person,role, project,n)   # ----------------

        d = date0()
        for i in range(n):
            tclass = ""
            color = "rgb(240,240,240)"
            if mon_outside_prj(d, project):
                color = "rgb(211,211,211)"
            elif dem_rj[i] > 0:
                color = "lightblue"
            else:
                tclass="color"
            a_w2[i] = {
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color,
                "class": tclass+" good",
                'up':up(c=wish)
            }
            d = inc(d)
        w2.append([{"class":"color",'up':up(c=wish),"val": project.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = "Все проекты"
    moon12["j"] = j
    moon12["r"] = r
    moon12["id"] = j
    return render(request, "needs_r.html", moon12)


''' 
доступность остаточная - персональная - один вид ресурса
'''
def rest_role(request:object, p:int, r:int, j:int,n:int=12)->object:
    moon12 = moon()
    dif14 = []
    dif15 = []
    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    people_rr = real_people(role)

    for person in people_rr:
        dif = time_available_person_role_12(person, role,n)

        dif100 = [0] * n
        da = date0()
        for i in range(n):
            dif100[i] = {
                "link": f"{person.id}.0.0.{da.year}-{da.month}-15",
                "up": up(1, 2),
                "title": dif[i],
            }  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    for person in people_rr:
        dif = rest_of_time_pr_12(person, role,n)

        dif100 = [0] * n
        da = date0()
        for i in range(n):
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

    return render(request, "rest_r.html", moon12)

'''
доступность максимальная - персональная - один вид ресурса
'''
def available_role(request:object, p:int, r:int, j:int,n:int=12)->object:
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
        dif = time_available_person_role_12(person, role,n)
        is100 = person_more_100_12(person)

        dif100 = [0] * n
        da = date0()
        for i in range(n):
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

    return render(request, "max_r.html", moon12)


'''
показать максимальную доступность по всем персонам и ролям
'''
def available_all(request:object,n:int=12)->object:  # Максимальная доступнасть по всем ресурсам

    moon12 = moon()
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()

    my = UserProfile.objects.all()
    arr = [0] * 100
    for p in my:
        arr[p.id] = [0] * 1000
        for r in roles:
            t = time_available_person_role_12(p, r,n)
            arr[p.id][r.id] = [0] * n
            for i in range(n):
                arr[p.id][r.id][i] += t[i]

    for role in roles:
        p9 = role.title
        people_rr = real_people(role)
        paint = Paint()
    #


        for person in people_rr:
            paint.next_row(person.fio)
            px = {"val": role.title, "r": role.id, "color": paint.rgb_back_left()}  ######################
            is100 = person_more_100_12(person,n)

            dif2 = [{"color":paint.rgb_back_right(),"val": person.fio}] + [0] * n
            dif = [person.fio] + time_available_person_role_12(person, role)
            d = date0()
            for i in range(n):
                paint.next_cell(dif[i + 1])
                dif2[i + 1] = {
                    "link": f"{person.id}.{role.id}.0.{d.year}-{d.month}-15",
                    "color": paint.color_rest(arr[person.id][role.id][i]),
                    "val": dif[i + 1],
                    "fire": is100[i],
                    "class":"good"
                }
                d = inc(d)

            dif14.append([px] + dif2)  ######################
           ##################################

    moon12["dif14"] = dif14  ########################################

    return render(request, "max.html", moon12)


'''
показать остаток ресурса по всем персонам и ролям
'''
def rest_all(request:object,n:int=12)->object:  # Остаточная доступость по всем ресурсам
    moon12 = moon()
    dif14 = []
    paint = Paint()
    project = None #Project.objects.all()
    roles = Role.objects.all()
    for role in roles:

        p9 = role.title
        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        px = role.title
        for person in people_rr:
            paint.next_row(None)
            dif = [{"color":paint.rgb_back_right(),
                    "val":person.fio}] + rest_and_color_12(person, role,paint.color_rest,12)
            dif14.append([{"color":paint.rgb_back_left(),"val":px}] + dif)


    moon12["dif14"] = dif14

    return render(request, "rest.html", moon12)


'''
портфель проектов
'''

def table_timeline(request:object,n:int=12)->object:  # все проекты (портфель)
    moon12 = moon()
    paint = Paint()
    projects = Project.objects.all().order_by("general", "start_date")
    data = []
    for p in projects:
        paint.next_row(None)
        data.append(project_timeline_line(p,paint))
    moon12["matrix"] = data
    return render(request, "prjlist.html", moon12)


import babel.dates
from datetime import date
'''
одна строка в портфель проектов
'''
import babel
def project_timeline_line(p,paint,n=12):

    dmin = date.today()
    dmin = dmin.replace(day=15)
    dmax = inc_n(dmin, n-1)
    L = []
    L.append({"val":p.general.fio,"color":paint.rgb_back_left()})
    L.append({"val": p.title, "id": p.id,"color":paint.rgb_back_right()})  # 989898

    formatted_date = babel.dates.format_date(p.start_date, "d MMM YY", locale='ru')
    L.append({"val": formatted_date,"color":paint.rgb_back_right()})

    formatted_date = babel.dates.format_date(p.end_date, "d MMM YY", locale='ru')
    L.append({"val": formatted_date, "color": paint.rgb_back_right()})


    L+= [{"val":timespan_len(p.start_date, p.end_date),"color": paint.rgb_back_right()}]
    L+= mon_bool_color(dmin, dmax, p.start_date, p.end_date,Paint.MY_BLUE,paint.rgb_back_right())
    return L

