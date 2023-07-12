from typing import List

from django.shortcuts import redirect, get_object_or_404, render

from .db import delta_role_project_12, needs_role_project_12, person_more_100_12, workload_role_project_12
from .db import get_prj_triplet, rest_of_time_pr_12, time_available_person_role_12
from .db import workload_person_role_project_12, real_and_virtual_people, real_people, rest_and_color_12
from .timing import timing_decorator
from .utils import *
from datetime import date
from .models import UserProfile, Grade, Wish,Project
from .utils import date0, inc, timespan_len, inc_n
from .view_forms import role_form
from django.urls import resolve
from .paint import Paint

'''
отсюда можно запускать тесты
'''
def atest(request:object)->object:
    roles = Role.objects.all()
    moon12 = available(roles, n=12)
    moon12["res"]="все ресурсы"
    return render(request, "a00.html",moon12)

def atest1(request:object)->object:
    return render(request, "a001.html")
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
    return workload_person_role_project_12(person, role, project, n)

'''
Объект Аутсорс - загрузка на год
'''
def outsrc(role:object, project:object,n:int=12)->List[int]:
    person = None
    try:
        person = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        pass
    return workload_person_role_project_12(person, role, project, n)


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
@timing_decorator
def balance_map(request:object, n:int)->object:
    projects = Project.objects.all()
    roles = Role.objects.all()
    xy = [0] * len(projects)
    for i in range(len(projects)):
        xy[i] = [0] * (len(roles) + 1)

    txy = [0] * len(roles)
    for j in range(len(roles)):
        txy[j] = {"val": roles[j].title, "link": f"/balance/{roles[j].id}/1/1/"}

    paint = Paint()
    for i in range(len(projects)):
        paint.next_row(projects[i])
        xy[i][0] = {"class":"even" if i%2==0 else "odd",
            "val": projects[i], "link": f"/balance/{projects[i].id}/0/1/"}

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
@timing_decorator
def table_projects(request:object)->object:
    # paint = Paint()
    projects = Project.objects.all().order_by("general")
    data = []
    for i in range(len(projects)):
        p = projects[i]
        data.append({"j": p.id, "project": p.title, "name": p.general.fio,
            "class":"odd" if (i % 2>0) else "even"})
             # })


    context = {"data": data}
    return render(request, "tab_j.html", context)

'''
Все ресурсы в одной таблице
'''
@timing_decorator
def table_resources(request:object)->object:
    # paint = Paint()
    context = {}
    data = []
    roles = Role.objects.all().order_by("general")
    for i in range(len(roles)):
        p = roles[i]
        data.append({"title": p.title, "r": p.id,
                     "class": "odd" if (i % 2>0) else "even",
                      "name":UserProfile.objects.get(user=p.general).fio})

    context["data2"] = data
    return render(request, "tab_r.html", context)

@timing_decorator
def people(request):
    context = {}
    profiles = UserProfile.objects.filter(virtual=False).order_by("fio")
    nx = len(Role.objects.all())
    data2 = []
    npLmax = 2
    i=0
    for profile in profiles:
        i=1-i
        try:
            grade1 = Grade.objects.filter(person=profile,role=profile.role).first().mygrade
        except:
            grade1 = '0'
        profile_data = {"fio": profile.fio, "role": profile.role,
                        "grade":grade1,
                        "class":"even" if i == 0 else "odd",
                        "res": [], "id": profile.id}
        pL = profile.res.all()

        for role in pL:
            if role != profile.role:
                grade = Grade.objects.filter(person=profile,role=role).first()
                grade_value = grade.mygrade if grade else '0'

                profile_data["res"].append({"role": str(role), "grade": grade_value,

                                            "id":role.id})


        data2.append(profile_data)
    context["data2"] = data2
    return render(request, "people.html", context)

@timing_decorator
def roles(request:object)->object:

    context = {}
    data = []
    roles = Role.objects.all().order_by("title")

    i=0
    for p in roles:

        m = {"title": p.title, "id": p.id, "general": p.general.userprofile.fio,
            "class":"even" if i==0 else "odd"
             }
        data.append(m)
    context["data2"] = data
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

def moon_exp(n:int=12)->List[object]:
    L = ['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек',]
    ym = []
    d = date0()
    for i in range(n):
         ym.append(f"{L[d.month-1]}_{str(d.year)[2:]}")
         d = inc(d)
    return  ym

def moon4(n: int = 12) -> List[object]:
        ym = []
        d = date0()
        for i in range(n):
            ym.append({"y": d.year, "m": d.month})
            d = inc(d)
        return {"ym": ym}


@timing_decorator
def available(roles,msg='',n=12):
    my = UserProfile.objects.all()
    arr = [0] * 100
    for p in my:
        arr[p.id] = [0] * 1000
        for r in roles:
            t = time_available_person_role_12(p, r, n)
            arr[p.id][r.id] = [0] * n
            for i in range(n):
                arr[p.id][r.id][i] += t[i]

    moon12 = moon()
    dif14 = []
    paint = Paint()
    i=0
    for role in roles:
        i=1-i
        people_rr = real_people(role)
        for person in people_rr:
            paint.next_row(person.fio)
            px = {"val": role.title, "r": role.id}
            is100 = person_more_100_12(person,n)

            dif2 = [{"val": person.fio,"align":"left"}] + [0] * n
            dif = [person.fio] + time_available_person_role_12(person, role)
            d = date0()
            for i in range(n):
                paint.next_cell(dif[i + 1])
                dif2[i + 1] = {"align":"center",
                    "link": f"{person.id}.{role.id}.0.{d.year}-{d.month}-15",
                    "color": paint.color_rest(arr[person.id][role.id][i]),
                    "val": dif[i + 1],
                    "fire": is100[i],
                    "class":"good"
                }
                d = inc(d)

            dif14.append([{"class":"odd" if i == 1 else "even"},px] + dif2)

    moon12["dif14"] = dif14  ########################################
    moon12["res"] = msg  ########################################
    return moon12

'''
доступность максимальная - персональная - один вид ресурса
'''
@timing_decorator
def available_role(request:object, r:int, n:int=12)->object:
    return redirect(to=f"/balance/{r}/0/5/")


def available_role2(request:object, r:int, n:int=12)->object:
    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    roles = [role]

    moon12 = available(roles,  n)
    moon12["res"]=role.title
    return render(request, "max.html", moon12)


'''
показать максимальную доступность по всем персонам и ролям
'''
@timing_decorator
def available_all(request:object,n:int=12)->object:  # Максимальная доступнасть по всем ресурсам
    roles = Role.objects.all()
    moon12 = available(roles, n=12)
    moon12["res"]="все ресурсы"
    moon12["ret"]="max"
    return render(request, "max.html", moon12)

def max_avl(request:object)->object:  # Максимальная доступнасть по всем ресурсам
    return redirect(request,"/balance/0/0/4/")



'''
показать остаток ресурса по вreсем персонам и ролям
'''
@timing_decorator
def rest_all(request:object,n:int=12)->object:  # Остаточная доступость по всем ресурсам
    return redirect(request,"/balance/0/0/6/")
    
    
def rest_all2(request:object,n:int=12)->object:  # Остаточная доступость по всем ресурсам
    moon12 = moon()
    dif14 = []
    roles = Role.objects.all().order_by('title')
    for role in roles:
        people_rr = real_people(role)
        dif = rest(role,people_rr)
        dif14+=dif

    moon12["dif14"] = dif14
    moon12["res"]="все ресурсы"
    return render(request, "rest.html", moon12)


''' 
доступность остаточная - персональная - один вид ресурса
'''


@timing_decorator
def rest_role(request:object, r:int,n:int=12)->object:
    return redirect(request,f"/balance/{id}/0/7/")

def rest_role2(request:object, r:int,n:int=12)->object:
    moon12 = moon()
    try:
        role = Role.objects.filter(id=r)[0]
    except:
        role = None

    people_rr = real_people(role)
    moon12["dif14"] = rest(role, people_rr, n)
    moon12["res"]=role.title
    return render(request, "rest.html", moon12)



def rest(role,people_rr, n = 12):

    dif10 = []

    paint = Paint()
    i=0
    for person in people_rr:
        i=1-i
        paint.next_row(None)
        dif = [{"align": "left","class": "even" if i==0 else "odd",
                "val": person.fio}] + rest_and_color_12(person, role, paint.color_rest, 12)
        dif10.append([{"class": "even" if i==0 else "odd", "val": role.title,
                       "align": "left", }] + dif)


    return dif10


'''
портфель проектов
'''
@timing_decorator
def table_timeline(request:object,n:int=12)->object:  # все проекты (портфель)
    moon12 = moon()
    paint = Paint()
    projects = Project.objects.all().order_by("general", "start_date")
    data = []
    i = 1
    for p in projects:
        i = 1-i
        paint.next_row(None)
        
        data.append([{"class":"even" if i==0 else "odd"
                      }]+project_timeline_line(p,paint))
    moon12["matrix"] = data
    return render(request, "prjlist.html", moon12)


def table_timeline_exp(request:object,n:int=12)->object:  # все проекты (портфель)
    moon12 = moon()
    projects = Project.objects.all().order_by("general", "start_date")
    data = []
    for p in projects:
        data.append(project_timeline_line_exp(p))
    return data

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
    L.append({"val":p.general.fio,
              # "color":paint.rgb_back_left(),
              "align":"left"})
    L.append({"val": p.title, "id": p.id,
              # "color":paint.rgb_back_right(),
              "align":"left"})  # 989898

    formatted_date = babel.dates.format_date(p.start_date, "d MMM YY", locale='ru')
    L.append({"val": formatted_date,
              # "color":paint.rgb_back_right(),
              "align":"left"})

    formatted_date = babel.dates.format_date(p.end_date, "d MMM YY", locale='ru')
    L.append({"val": formatted_date,
              # "color": paint.rgb_back_right(),
              "align":"left"})


    L+= [{"val":timespan_len(p.start_date, p.end_date),
          # "color": paint.rgb_back_right(),
          "align":"center"}]

    L+= mon_bool_color(dmin, dmax, p.start_date, p.end_date,Paint.MY_BLUE,'')
    return L

def project_timeline_line_exp(p,n=12):

    dmin = date.today()
    dmin = dmin.replace(day=15)
    dmax = inc_n(dmin, n-1)
    L = []
    L+=[p.general.fio, p.title, ]

    formatted_date1 = babel.dates.format_date(p.start_date, "d MMM YY", locale='ru')
    L+=[formatted_date1]
           

    formatted_date2 = babel.dates.format_date(p.end_date, "d MMM YY", locale='ru')
    L+= [formatted_date2]

    L+= [timespan_len(p.start_date, p.end_date)]

    L+= mon_bool_exp(dmin, dmax, p.start_date, p.end_date)
    return L
