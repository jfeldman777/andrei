'''
назначения - один ресурс - один проект
'''
from django.shortcuts import render

from .db import get_prj_triplet, delta_role_project_12, real_and_virtual_people, needs_role_project_12, \
    task_person_role_project_12, rest_of_time_pr_12
from .models import Wish, Grade, Role, Project
from .paint import Paint
from .utils import date0, inc, up
from .vvv import moon


def task_role_project(request: object, p: int, r: int, j: int, n: int = 12) -> object:
    person, role, project = get_prj_triplet(-1, r, j)
    try:
        wish = Wish.objects.get(role=role, project=project, ).mywish
    except:
        wish = ''
    w3 = []

    moon12 = moon()
    delta = delta_role_project_12(role, project, n)
    people = real_and_virtual_people(role)
    dem_rj = needs_role_project_12(person, role, project, n)  # ----------------
    paint3 = Paint()
    for person in people:
        paint3.next_row(None)
        if person == None:
            break
        b_w3 = [0] * n
        a_w3 = task_person_role_project_12(person, role, project, n)
        diff = rest_of_time_pr_12(person, role)
        d = date0()
        try:
            p = person.id
        except:
            p = 0
        for i in range(n):
            paint3.next_row(None)

            try:
                df = diff[i]
            except:
                df = 0
            isOut = d < project.start_date or d > project.end_date
            isPurple = delta[i] < 0
            b_w3[i] = {
                "link": f"{p}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(max(-delta[i], 0), df, wish),
                "val": a_w3[i],
                "color": paint3.color_tasks(isOut,isPurple),
                "fire": df < 0,
                "class": "  good"
            }
            d = inc(d)
        up1 = ''
        if not person.virtual:
            try:
                grade = Grade.objects.get(person=person, role=role).mygrade
            except:
                grade = '0'
            up1 = f" ({grade})"
        c_w3 = [{'color': paint3.rgb_back_left(), "val": person.fio + up1}] + b_w3

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


def task_project(request: object, p: int, r: int, j: int, n: int = 12) -> object:
    person, role, project = get_prj_triplet(-1, -1, j)
    w3 = []

    moon12 = moon()
    paint3 = Paint()
    roles = Role.objects.all()
    for role in roles:

        try:
            wish = Wish.objects.get(role=role, project=project, ).mywish
        except:
            wish = ''
        delta = delta_role_project_12(role, project, n)
        people = real_and_virtual_people(role)
        dem_rj = needs_role_project_12(person, role, project, n)  # ----------------

        p100 = {"val": role.title}
        for person in people:
            paint3.next_row(None)
            diff = rest_of_time_pr_12(person, role, n)
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project, n)

            d = date0()
            for i in range(n):
                paint3.next_cell(a_w3[i])

                isOut = d < project.start_date or d > project.end_date
                isPurple = delta[i] < 0

                t = paint3.color_tasks(isOut,isPurple)
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i], wish),
                    "val": a_w3[i],
                    "color": t,
                    "fire": diff[i] < 0,
                    'class': "  good"
                }
                d = inc(d)

            up1 = ''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100, {'color': paint3.rgb_back_left(), "val": person.fio + up1}] + b_w3

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


def task_role(request: object, p: int, r: int, j: int, n: int = 12) -> object:
    person, role, project = get_prj_triplet(-1, r, -1)

    w3 = []
    moon12 = moon()
    people = real_and_virtual_people(role)
    projects = Project.objects.all()

    for project in projects:
        try:
            wish = Wish.objects.get(role=role, project=project, ).mywish
        except:
            wish = ''
        delta = delta_role_project_12(role, project, n)

        paint3 = Paint()
        for person in people:
            paint3.next_row(None)
            p100 = {"val": project.title,'color':paint3.rgb_back_left()}
            b_w3 = [0] * n
            a_w3 = task_person_role_project_12(person, role, project, n)
            diff = rest_of_time_pr_12(person, role, n)
            d = date0()
            for i in range(n):

                isOut = d < project.start_date or d > project.end_date
                isPurple = delta[i] < 0
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(max(-delta[i], 0), diff[i], wish),
                    "val": a_w3[i],
                    "color": paint3.color_tasks(isOut,isPurple),
                    "fire": diff[i] < 0,
                    "class": "good"
                }
                d = inc(d)

            up1 = ''
            if not person.virtual:
                try:
                    grade = Grade.objects.get(person=person, role=role).mygrade
                except:
                    grade = '0'
                up1 = f" ({grade})"
            c_w3 = [p100, {'color':paint3.rgb_back_right(),"val": person.fio + up1}] + b_w3
            w3.append(c_w3)

    moon12["w3"] = w3
    moon12["role"] = role
    moon12["project"] = project
    moon12["r"] = r
    moon12["j"] = j
    return render(request, "tasks_r.html", moon12)