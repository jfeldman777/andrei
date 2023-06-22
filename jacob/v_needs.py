
'''
потребность - ресурс один - проекты все
'''
from datetime import date

from django.shortcuts import render

from .db import get_prj_triplet, delta_role_project_12, needs_role_project_12
from .models import Project, Wish, Role
from .paint import Paint
from .utils import date0, inc, up
from .vvv import moon, home


def needs_role(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, r, -1)

    w2 = []
    moon12 = moon()
    paint2 = Paint()
    projects = Project.objects.all().order_by('title')

    for project in projects:
        paint2.next_row(None)
        try:
            wish = Wish.objects.get(project=project,role=role)
        except:
            wish = None

        delta = delta_role_project_12(role, project,n)

        a_w2 = [0] * n
        dem_rj = needs_role_project_12(person,role, project,n)   # ----------------

        d = date0()
        for i in range(n):
            paint2.next_cell(dem_rj[i])
            a_w2[i] = {
                "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": paint2.color_needs(project.start_date,project.end_date,d),
                "class": " good",
                'up':up(c=wish)
            }
            d = inc(d)
        w2.append([{"color":paint2.rgb_back_left(),'up':up(c=wish)+"?","class":"wish",
                    "project":project.id,"role":r,
                    "val": project.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = "Все проекты"
    moon12["j"] = j
    moon12["r"] = r
    moon12["id"] = j
    return render(request, "needs_r.html", moon12)



'''
потребность - прект один  -ресурсы все
'''
def needs_project(request:object, p:int, r:int, j:int,n:int=12)->object:
    person, role, project = get_prj_triplet(-1, -1, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all().order_by('title')
    paint2 = Paint()

    for role in roles:
        paint2.next_row(None)
        try:
            wish = Wish.objects.get(role=role,project=project,).mywish
        except:
            wish=''
        delta = delta_role_project_12(role, project)

        a_w2 = [0] * n
        dem_rj = needs_role_project_12(person,role, project,n)  # ----------------

        d = date.today().replace(day=15)

        for i in range(n):
            paint2.next_cell(dem_rj[i])
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": paint2.color_needs(project.start_date,project.end_date,d),
                "class":"  good",
                'up':up(c=wish)
            }
            d = inc(d)
        w2.append([{"color":paint2.rgb_back_left(),"class":"wish",
                    'up':up(c=wish)+'?',"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = "Все ресурсы"

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = 0
    moon12["id"] = j
    return render(request, "needs_j.html", moon12)


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
    paint2 = Paint()
    paint2.next_row(None)
    for i in range(n):
        paint2.next_cell(dem_rj[i])
        a_w2[i] = {
            "link": f"0.{r}.{j}.{d.year}-{d.month}-15",
            "val": dem_rj[i],
            "color":paint2.color_needs(project.start_date,project.end_date,d),

            "class": "  good",
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
