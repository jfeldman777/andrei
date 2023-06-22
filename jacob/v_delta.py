

'''
дельта - один ресурс - один проект
'''
from django.shortcuts import render

from .db import delta_role_project_12, get_prj_triplet, rest_of_time_pr_12, task_person_role_project_12, \
    real_people, real_and_virtual_people, rest_and_color_12, needs_role_project_12
from .models import Wish, Grade, Project, Role
from .paint import Paint
from .utils import date0, inc, up
from .vvv import moon


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

    paint2 = Paint()
    d = date0()
    paint2.next_row(None)
    for i in range(n):
        paint2.next_cell(dem_rj[i])

        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color": paint2.color_needs(project.start_date,project.end_date,d),
            "class":"good"
        }  #

        d = inc(d)
    w2 = a_w2
    paint3 = Paint()
    for person in people_rv:
        paint3.next_row(None)
        if person == None:
            break
        b_w3 = [0] * n
        a_w3 = task_person_role_project_12(person, role, project,n)
        diff = rest_of_time_pr_12(person, role,n)
        d = date0()
        for i in range(n):
            paint3.next_cell(a_w3[i])
            try:
                p = person.id
                df = diff[i]
            except:
                p = 0
                df = 0
            isOut = d < project.start_date or d > project.end_date
            isPurple = delta[i] < 0
            b_w3[i] = {
                "link": f"{p}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i], 0), df),
                "val": a_w3[i],
                "color": paint3.color_tasks(isOut, isPurple),
                "class":"good ",
            }
            d = inc(d)

        up1 = ''
        if not person.virtual:
            try:
                grade = Grade.objects.get(person=person, role=role).mygrade
            except:
                grade = '0'
            up1=f" ({grade})"
        c_w3 = [{"color":paint3.rgb_back_left(),"val": person.fio + up1}] + b_w3
        p100 = -1
        w3.append(c_w3)
    paint1 = Paint()
    paint1.next_row(None)
    w1.append(paint1.plus_color_balance(delta))  ############################
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
    paint2 = Paint()
    paint1 = Paint()
    paint3 = Paint()
    for project in projects:
        paint1.next_row(None)
        paint2.next_row(None)
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
                "color":paint2.rgb_back_left()
            }
        ] + [0] * n

        dem_rj = [project.title] + ["Потребность"] + needs_role_project_12(person,role, project,n)   #
        delta = delta_role_project_12(role, project,n)
        d = date0()
        for i in range(n):
            paint2.next_cell(dem_rj[i+2])
            isOut = d < project.start_date or d > project.end_date
            isPurple = delta[i] < 0
            a_w2[i + 1] = {
                "val": dem_rj[i + 2],
                "j": project.id,
                "r": role.id,
                "color": paint3.color_tasks(isOut,isPurple),
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "class": "  good"
            }
            d = inc(d)
        w2.append(a_w2)  # --------



        for person in people_rv:
            paint3.next_row(None)
            diff = rest_of_time_pr_12(person, role,n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)

            d = date0()

            for i in range(n):
                paint3.next_cell(a_w3[i])
                isOut = d < project.start_date or d > project.end_date
                isPurple = delta[i] < 0
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": paint3.color_tasks(isOut, isPurple),
                    "class": "  good"
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
            c_w3 = [p100,{"color":paint3.rgb_back_left(),"val": person.fio + up1}] + b_w3
            p100 = -1
            w3.append(c_w3)


        w1.append(paint1.plus_color_balance([ project.title] + delta)  )

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
    paint2 = Paint()
    paint1 = Paint()
    for role in roles:
        paint2.next_row(None)
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
            paint2.next_cell(dem_rj[i])

            a_w2[i] = {
                "val": dem_rj[i],

                "color": paint2.color_needs(project.start_date, project.end_date, d),
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "class":"  good"
            }

            d = inc(d)
        w2.append(
            [
                {
                    "r": role.id,
                    "j": project.id,
                    "val": role.title,
                    "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                    "color":paint2.rgb_back_left()
                }
            ]
            + a_w2
        )
        paint3 = Paint()
        p100 = role.title
        for person in people_rv:
            paint3.next_row(None)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project,n)
            diff = rest_of_time_pr_12(person, role,n)
            d = date0()
            for i in range(n):
                paint3.next_cell(a_w3[i])
                isOut = d < project.start_date or d > project.end_date
                isPurple = delta[i] < 0
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": paint3.color_tasks(isOut,isPurple),
                    "class":"  good"
                }
                d = inc(d)

            up1=''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100,{'color': paint3.rgb_back_left(), "val": person.fio + up1}] + b_w3
            p100 = -1
            w3.append(c_w3)

        paint1.next_row(None)
        w1.append(paint1.plus_color_balance([role.title] + delta))
        ############################
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