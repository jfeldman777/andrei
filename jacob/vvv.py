from .models import Less
from .forms import EntryForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
def up(a, b):
    return f"надо:{a}/есть:{b}"

def demm(r, j, n):
    rjd = rj_load_(r, j)
    sum = 0
    for i in range(n):
        sum += rjd[i]
    if sum == 0:
        return 1
    return sum


def dell(r, j, n):
    rjd = rj_delta_(r, j)
    sum = 0
    for i in range(n):
        if rjd[i] < 0:
            sum -= rjd[i]
    return sum


def n2txt(n):
    if n == 1:
        return "на 1 месяц"
    if n == 3:
        return "на 3 месяца"
    return f"на {n} месяцев"


def b(request, n):
    projects = Project.objects.all()
    roles = Role.objects.all()
    xy = [0] * len(projects)
    for i in range(len(projects)):
        xy[i] = [0] * (len(roles) + 1)

    txy = [0] * len(roles)
    for j in range(len(roles)):
        txy[j] = {
            "val": roles[j].title, "link": f"/dr/0/{roles[j].id}/0/"}

    for i in range(len(projects)):
        xy[i][0] = {"val": projects[i],
                    "link": f"/dj/0/0/{projects[i].id}/"
                    }
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

            xy[i][j + 1] = {"val": f"{x}%",
                            "link": f"/djr/0/{roles[j].id}/{projects[i].id}/",
                            "color": color,
                            "i": project.id,
                            "j": role.id}
    context = {"tab": xy, "txy": txy, "n": n, "hh": n2txt(n)}

    return render(request, 'b.html', context)


def p_101(person):
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


def mj_outside(m, j):
    d1 = j.start_date
    d2 = j.end_date
    return not (d1 <= m and m <= d2)


def get_prj(p, r, j):
    role = None
    if r > 0:
        role = Role.objects.get(id=r)
    person = None
    if p > 0:
        person = UserProfile.objects.get(id=p)
    project = None
    if j > 0:
        project = Project.objects.get(id=j)

    return (person, role, project)


def people_of_rv(role):
    pp1 = set(UserProfile.objects.filter(Q(role=role)))
    pp2 = set(UserProfile.objects.filter(Q(res=role)))
    return pp1.union(pp2)


def people_of_rr(role):
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    return pp1.union(pp2)


def prjm_task(request, p, r, j, y, m):
    d = date(y, m, 15)  # .replace(year=y).replace(month=m).replace(day=15)
    person, role, project = get_prj(p, r, j)
    task = Task.objects.filter(project=project, person=person, role=role, month=d)
    context = {"t": task}
    return render(request, 'a_test.html', context)


def prm_isfree(request, p, r, y, m):
    res = prm_isfree_(p, r, y, m)
    context = {"t": res}
    return render(request, 'a_test.html', context)


def prm_isfree_(p, r, y, m):
    d = date(y, m, 15)  # .replace(year=y).replace(month=m).replace(day=15)
    person, role, project = get_prj(p, r, -1)
    if person.role == role:
        t = 100
    elif role in person.res:
        t = 0
    task = Less.objects.filter(person=person, role=role, start_date__lte=d).order_by('-start_date')
    try:
        t = task[0].load
    except:
        pass
    return t


def rjm_load(request, r, j, y, m):
    d = date(y, m, 15)  # .replace(year=y).replace(month=m).replace(day=15)
    person, role, project = get_prj(-1, r, j)
    task = Load.objects.filter(project=project, role=role, month=d)
    context = {"t": task}
    return render(request, 'a_test.html', context)


def rj_dif_(p, r, j):
    res = [0] * 12
    load = pr_isfree_(p, r)
    task = rj_task_(r, j)
    for i in range(12):
        res[i] = load[i] - task[i]

    return res


def pr_dif(request, p, r):
    t = pr_dif_(p, r)
    context = {"t": t}
    return render(request, 'a_test.html', context)


def pr_dif_(p, r):
    c = [0] * 12
    a = pr_task_(p, r)
    b = pr_isfree_(p, r)
    for i in range(12):
        c[i] = b[i] - a[i]
    return c


def pr_task(request, p, r):
    res = pr_task_(p, r)
    context = {"t": res}
    return render(request, 'a_test.html', context)


def pr_task_(person, role):
    d = date.today().replace(day=15)
    res = [0] * 12
    for i in range(12):
        tasks = Task.objects.filter(person=person, role=role, month=d)
        for task in tasks:
            try:
                res[i] += task.load
            except:
                pass
        d = inc(d)
    return res


def vacancia(role, project):
    person = UserProfile.objects.get(id=11)
    return prj_task_(person, role, project)


def outsrc(role, project):
    person = UserProfile.objects.get(id=10)
    return prj_task_(person, role, project)


def prm_task(request, p, r, y, m):
    d = date(y, m, 15)
    t = 0
    person, role, project = get_prj(p, r, -1)

    tasks = Task.objects.filter(person=person, role=role, month=d)
    for task in tasks:
        try:
            t += task.load
        except:
            pass

    context = {"t": t}
    return render(request, 'a_test.html', context)


def prj_task(request, p, r, j):
    person, role, project = get_prj(p, r, j)
    res = prj_task_(person, role, project)
    context = {"t": res}
    return render(request, 'a_test.html', context)


def prj_task_(p, r, j):
    d = date.today().replace(day=15)
    res = [0] * 12
    for i in range(12):
        t = Task.objects.filter(person=p, project=j, role=r, month=d)
        try:
            res[i] += t[0].load
        except:
            pass
        d = inc(d)
    return res


def rj_task_v(r, j):
    d = date.today().replace(day=15)
    res = [0] * 12
    for i in range(12):
        tasks = Task.objects.filter(project=j, role=r, month=d)
        for t in tasks:
            try:
                res[i] += t.load
            except:
                pass
        d = inc(d)
    return res


def rj_task_(r, j):
    d = date.today().replace(day=15)
    res = [0] * 12
    for i in range(12):
        tasks = Task.objects.filter(project=j, role=r, month=d)
        for t in tasks:
            if t.person.id not in (10, 11):
                try:
                    res[i] += t.load
                except:
                    pass
        d = inc(d)
    return res


def pr_isfree(request, p, r):
    res = pr_isfree_(p, r)
    context = {"t": res}
    return render(request, 'a_test.html', context)


def pr_isfree_(person, role):
    res = [0] * 12
    d = date.today().replace(day=15)  # .replace(year=y).replace(month=m).replace(day=15)
    t = -1
    if person.role == role:
        t = 100
    elif person.res.filter(id=role.id).exists():
        t = 0

    for i in range(12):
        task = Less.objects.filter(person=person, role=role, start_date__lte=d).order_by('-start_date')
        try:
            t = task[0].load
        except:
            pass
        res[i] = t
        d = inc(d)
    return res


def rj_isfree_(role, project):
    people = people_of_rr(role)
    res = [0] * 12
    for person in people:
        isfree = pr_isfree_(person, role)
        for i in range(12):
            res[i] += isfree[i]
    return res


def rj_load(request, r, j):
    person, role, project = get_prj(-1, r, j)
    res = rj_load_(role, project)
    context = {"t": res}
    return render(request, 'a_test.html', context)


def rj_load_(r, j):
    d = date.today().replace(day=15)
    res = [0] * 12
    for i in range(12):
        t = Load.objects.filter(project=j, role=r, month=d)
        try:
            res[i] = t[0].load
        except:
            pass
        d = inc(d)
    return res


def rj_delta_(r, j):
    a = rj_load_(r, j)
    b = rj_task_v(r, j)
    c = [0] * 12
    for i in range(12):
        c[i] = b[i] - a[i]
    return c


def date0():
    d = date.today().replace(day=15)
    return d


def date12():
    d = date.today().replace(day=15)
    d = inc_n(d, 12)
    return d


def atest(request):
    project = Project.objects.get(id=2)
    print (project)
    return render(request, 'a_test.html')


def alf(request):
    p = None
    r = None
    project = '?'
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['projects']
            roles = form.cleaned_data['roles']
            if project:
                p = Project.objects.get(title=project)
            if roles:
                r = Role.objects.get(title=roles)

            return ajr(request, p.id, r.id, 1)

    form = EntryForm()
    return render(request, 'alf.html', {'form': form})


def atj(request):
    projects = Project.objects.all().order_by('general')
    data = []
    for p in projects:
        x = {"j": p.id,
             "project": p.title,
             "name": p.general.fio}
        data.append(x)
    context = {"data": data}

    return render(request, 'atj.html', context)


def atr(request):
    context = {}
    roles = Role.objects.all().order_by('general')
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {
            "title": p.title, "r": p.id,
            "name": u.fio}
        data2.append(x)
    context["data2"] = data2

    return render(request, 'atr.html', context)


def att(request):
    projects = Project.objects.all().order_by('general')
    data = []
    for p in projects:
        x = {"j": p.id,
             "project": p.title,
             "name": p.general.fio}
        data.append(x)
    context = {"data": data}

    roles = Role.objects.all().order_by('general')
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {
            "title": p.title, "r": p.id,
            "name": u.fio}
        data2.append(x)
    context["data2"] = data2

    return render(request, 'att.html', context)


def a00(request):
    return render(request, 'a00.html')


def zero(name):
    sum = [name] + [0] * 12
    return sum


def diffx(person, role):
    return pr_dif_(person, role)


def moon():
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
    person, role, project = get_prj(-1, r, j)
    w3 = []

    moon12 = moon()
    delta = rj_delta_(role, project)

    people = people_of_rv(role)
    dem_rj = rj_load_(role, project)  # ----------------

    for person in people:
        b_w3 = [0] * 12
        a_w3 = prj_task_(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            b_w3[i] = {
                "link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(
                    max(-delta[i], 0)
                    , diff[i]),
                "val": a_w3[i],
                "color": color

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
    return render(request, 'ujr.html', moon12)


def uj(request, p, r, j):
    person, role, project = get_prj(-1, -1, j)
    w3 = []

    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:

        delta = rj_delta_(role, project)

        people = people_of_rv(role)
        dem_rj = rj_load_(role, project)  # ----------------
        p100 = {"val": role.title}
        for person in people:
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)

            d = date.today().replace(day=15)
            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                b_w3[i] = {"link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                           "up": up(
                               max(-delta[i], 0)
                               , diff[i]),
                           "val": a_w3[i],
                           "color": color

                           }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

    moon12["w3"] = w3

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = role.id
    moon12["j"] = j
    return render(request, 'uj.html', moon12)


def ur(request, p, r, j):
    person, role, project = get_prj(-1, r, -1)
    w3 = []

    moon12 = moon()
    delta = rj_delta_(role, project)

    people = people_of_rv(role)
    projects = Project.objects.all()

    for project in projects:
        p100 = {"val": project.title}
        for person in people:
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)
            diff = pr_dif_(person, role)
            d = date.today().replace(day=15)
            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                elif delta[i] > 0:
                    color = "lightblue"
                    
                b_w3[i] = {"link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                           "up": up(
                               max(-delta[i], 0)
                               , diff[i]),
                           "val": a_w3[i],
                           "color": color

                           }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

    moon12["w3"] = w3

    moon12["role"] = role

    moon12["project"] = project

    moon12["r"] = r

    return render(request, 'ur.html', moon12)


def djr(request, p, r, j):
    person, role, project = get_prj(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    delta = rj_delta_(role, project)

    w4 = []

    people_rv = people_of_rv(role)
    people_rr = people_of_rr(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + pr_dif_(person, role))

    a_w2 = [0] * 12
    dem_rj = rj_load_(role, project)  # ----------------

    d = date.today().replace(day=15)
    for i in range(12):
        color="white"
        if mj_outside(d, project):
            color = "lightgrey"
        elif dem_rj[i]>0:
            color = "lightblue"
        a_w2[i] = {"link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15", "val": dem_rj[i],

                   "color": color,

                   }  #

        d = inc(d)
    w2 = a_w2

    for person in people_rv:
        b_w3 = [0] * 12
        a_w3 = prj_task_(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            b_w3[i] = {
                "link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15",
                "up": up(
                    max(-delta[i], 0)
                    , diff[i]),
                "val": a_w3[i],
                "color": color

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
    return render(request, 'djr.html', moon12)


# Дельта, один проект, один ресурс
def ajr(request, p, r, j):  # Альфа, один проект, один ресуря
    person, role, project = get_prj(-1, r, j)

    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    supp = [-1, 'Поставка'] + rj_task_(role, project)
    delta = ['Дельта'] + rj_delta_(role, project)
    zo = ['АУТСОРС'] + outsrc(role, project)
    zv = ['ВАКАНСИЯ'] + vacancia(role, project)
    w4 = []

    people_rr = people_of_rr(role)
    people_rv = people_of_rv(role)

    for person in people_rr:  # 7777777777777777777777777777777777777777
        w4.append([person.fio] + pr_dif_(person, role))

    a_w2 = [0] * 12
    dem_rj = ['Потребность'] + rj_load_(role, project)  # ----------------

    d = date.today().replace(day=15)
    for i in range(12):
        color="white"
        if mj_outside(d, project):
            color = "lightgrey"
        elif dem_rj[i+1]>0:
            color = "lightblue"
        a_w2[i] = {"link": f"0.{r}.{j}.{d.year}-{d.month}-15",
                   "val": dem_rj[i + 1],

                   "color": color,

                   }  #

        d = inc(d)
    w2 = a_w2

    supp = ['Поставка'] + rj_task_(role, project)
    delta = ['Дельта'] + rj_delta_(role, project)

    for person in people_rv:
        b_w3 = [0] * 12
        a_w3 = prj_task_(person, role, project)
        diff = pr_dif_(person, role)
        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
                if delta[i] < 0:
                    color = "#B266FF"
            elif delta[i] < 0:
                color = "pink"
            b_w3[i] = {"link": f"{person.id}.{r}.{j}.{d.year}-{d.month}-15",
                       "up": up(
                           max(-delta[i + 1], 0)
                           , diff[i]),
                       "val": a_w3[i],
                       "color": color

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
    return render(request, 'ajr.html', moon12)


def ar(request, p, r, j):
#    print(888,p,r,j)
#    role = Role.objects.get(id=r)
    person, role, project = get_prj(-1, r, -1)
    people_rr = people_of_rr(role)
    people_rv = people_of_rv(role)
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    projects = Project.objects.all()

    zo = ['АУТСОРС'] + outsrc(role, project)
    zv = ['ВАКАНСИЯ'] + vacancia(role, project)
    # W222222222222222222222222222222
    for project in projects:

        a_w2 = [{"val": project.title, "j": project.id, "r": r}] + [0] * 12
        dem_rj = [project.title] + ['Потребность'] + rj_load_(role, project)  #

        d = date.today().replace(day=15)
        for i in range(12):
            color="white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i+2]>0:
                color = "lightblue"
            a_w2[i + 1] = {"val": dem_rj[i + 2],
                           "color": color,
                           "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",

                           }  # 9898
            d = inc(d)
        w2.append(a_w2)  # --------

        supp = ['Поставка'] + rj_task_(role, project)
        delta = ['Дельта'] + rj_delta_(role, project)

        w4 = []

        x = [0] * 12
        p200 = project.title
        for person in people_rr:
            diff = pr_dif_(person, role)
            x = diff
            w4.append([person.fio] + x)


        p100 = project.title
        for person in people_rv:
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)
            diff = pr_dif_(person, role)
            d = date.today().replace(day=15)
            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i+1] < 0:
                        color = "#B266FF"
                elif delta[i+1] < 0:
                    color = "pink"
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(
                        max(-delta[i + 1], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color

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

    moon12["project"] = project
    moon12["role"] = role

    moon12["r"] = r
    moon12["j"] = 0
    moon12["p"] = 0
    return render(request, 'ar.html', moon12)


def dr(request, p, r, j):
    person, role, project = get_prj(-1, r, -1)

    people_rr = people_of_rr(role)
    people_rv = people_of_rv(role)
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()
    projects = Project.objects.all()

    # W222222222222222222222222222222
    for project in projects:
        a_w2 = [{"val": project.title,
                 "j": project.id,
                 "r": role.id,
                 }] + [0] * 12

        dem_rj = [project.title] + ['Потребность'] + rj_load_(role, project)  #

        d = date.today().replace(day=15)
        for i in range(12):
            color="white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i+2]>0:
                color = "lightblue"
            a_w2[i + 1] = {"val": dem_rj[i + 2],
                           "j": project.id,
                           "r": role.id,
                           "color": color,
                           "link": f"0.{r}.{project.id}.{d.year}-{d.month}-15",
                           }
            d = inc(d)
        w2.append(a_w2)  # --------

        delta = rj_delta_(role, project)

        w4 = []

        x = [0] * 12
        p100 = project.title
        for person in people_rr:
            diff = pr_dif_(person, role)
            x = diff
            w4.append([person.fio] + x)

        for person in people_rv:
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)

            d = date.today().replace(day=15)

            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                b_w3[i] = {
                    "link": f"{person.id}.{r}.{project.id}.{d.year}-{d.month}-15",
                    "up": up(
                        max(-delta[i], 0), diff[i]),
                    "val": a_w3[i],
                    "color": color

                }
                ##########################################################################3333333
                d = inc(d)
            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        delta2 = [{"val": x} for x in delta]
        # w1.append([project.title]+delta)############################
        w1.append([{"j": project.id, "val": project.title}] + delta2)  ############################

    moon12["w4"] = w4  ########################################
    moon12["w2"] = w2  #####################
    moon12["w1"] = w1  ###############################
    moon12["w3"] = w3

    moon12["role"] = role
    moon12["r"] = r
    moon12["j"] = 0
    moon12["p"] = 0
    moon12["project"] = project

    return render(request, 'dr.html', moon12)


def dj(request, p, r, j):  # Дельта, один проект все ресурсы
    person, role, project = get_prj(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    w4 = []

    roles = Role.objects.all()
    for role in roles:

        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)
        p6 = role.title
        for person in people_rr:  # 7777777777777777777777777777777777777777
            diff = pr_dif_(person, role)
            w4.append([p6, person.fio] + diff)
            p6 = -1

        delta = rj_delta_(role, project)

        a_w2 = [0] * 12
        dem_rj = rj_load_(role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color="white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i]>0:
                color = "lightblue"

            a_w2[i] = {
                "val": dem_rj[i],"color":color,
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
            }

            d = inc(d)
        w2.append([
                      {"r": role.id, "j": project.id,
                       "val": role.title,
                       "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                       "color": color
                       }

                  ] + a_w2)

        p100 = role.title
        for person in people_rv:
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)
            diff = pr_dif_(person, role)
            d = date.today().replace(day=15)
            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i] < 0:
                        color = "#B266FF"
                elif delta[i] < 0:
                    color = "pink"
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(
                        max(-delta[i], 0)
                        , diff[i]),
                    "val": a_w3[i], "color": color

                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        delta2 = [{"val": x} for x in delta]
        w1.append([{"r": role.id, "val": role.title}] + delta2)  ############################
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
    return render(request, 'dj.html', moon12)


def aj(request, p, r, j):  # Альфа, один проект
    person, role, project = get_prj(-1, -1, j)
    w4 = []
    w3 = []
    w2 = []
    w1 = []
    moon12 = moon()

    w4 = []

    roles = Role.objects.all()
    a_w2 = [0] * 12
    for role in roles:
        zo = ['АУТСОРС'] + outsrc(role, project)
        zv = ['ВАКАНСИЯ'] + vacancia(role, project)
        supp = ['Поставка'] + rj_task_(role, project)
        delta = ['Дельта'] + rj_delta_(role, project)
        dem_rj = rj_load_(role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i]>0:
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
        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)
        for person in people_rr:  #
            diff = pr_dif_(person, role)
            w4.append([p200, person.fio] + diff)
            p200=-1
        for person in people_rv:  #
            diff = pr_dif_(person, role)
            b_w3 = [0] * 12
            a_w3 = prj_task_(person, role, project)

            d = date.today().replace(day=15)
            for i in range(12):
                color = "white"
                if mj_outside(d, project):
                    color = "lightgrey"
                    if delta[i+1] < 0:
                        color = "#B266FF"
                elif delta[i+1] < 0:
                    color = "pink"
                b_w3[i] = {
                    "link": f"{person.id}.{role.id}.{j}.{d.year}-{d.month}-15",
                    "up": up(
                        max(-delta[i + 1], 0)
                        , diff[i]),
                    "val": a_w3[i],
                    "color": color

                }
                d = inc(d)

            c_w3 = [p100, {"val": person.fio}] + b_w3
            p100 = -1
            w3.append(c_w3)

        w1.append([role.title, 'Потребность'] + dem_rj)  ##########################################77777
        w1.append([-1] + supp)  ###############--
        w1.append([-1] + zo)  ################
        w1.append([-1] + zv)  #####################
        w1.append([-1] + delta)  ############################
    moon12["w1"] = w1
    moon12["w2"] = w2
    moon12["w3"] = w3
    moon12["w4"] = w4

    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = role.id
    moon12["j"] = j

    moon12["p"] = 0
    return render(request, 'aj.html', moon12)  # АЛьфа, один проект все ресурсы


def mmjr(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj(-1, r, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:

        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)

        delta = rj_delta_(role, project)

        a_w2 = [0] * 12
        dem_rj = rj_load_(role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i]>0:
                color = "lightblue"
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],

                "color": color
            }
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = role.id
    moon12["id"] = j
    return render(request, 'mmjr.html', moon12)


def mmj(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj(-1, -1, j)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        # diff = rj_dif_(None,role, project)
        # people_rr = people_of_rr(role)
        # people_rv = people_of_rv(role)

        delta = rj_delta_(role, project)

        a_w2 = [0] * 12
        dem_rj = rj_load_(role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color = "white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i]>0:
                color = "lightblue"
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],

                "color": color
            }
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = role.id
    moon12["id"] = j
    return render(request, 'mmj.html', moon12)


def mmr(request, p, r, j):  # Потребность на малом экране
    person, role, project = get_prj(-1, r, -1)

    w2 = []
    moon12 = moon()

    roles = Role.objects.all()
    for role in roles:
        diff = rj_dif_(role, project)
        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)

        delta = rj_delta_(role, project)

        a_w2 = [0] * 12
        dem_rj = rj_load_(role, project)  # ----------------

        d = date.today().replace(day=15)
        for i in range(12):
            color="white"
            if mj_outside(d, project):
                color = "lightgrey"
            elif dem_rj[i]>0:
                color = "lightblue"
            a_w2[i] = {
                "link": f"0.{role.id}.{j}.{d.year}-{d.month}-15",
                "val": dem_rj[i],
                "color": color
            }
            d = inc(d)
        w2.append([{"val": role.title}] + a_w2)

    moon12["w2"] = w2

    moon12["role"] = role

    moon12["project"] = project
    moon12["j"] = j
    moon12["r"] = role.id
    moon12["id"] = j
    return render(request, 'mmr.html', moon12)


#########################################################################Альфа, один ресурс, все проекты
def smr(request):  # доступность
    id = 1
    r=1
    p=1
    j=1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        if form.is_valid():

            for k, v in request.POST.items():

                if '.' in k:
                    p, r, j, d = k.split('.')

                    try:
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)

                        tr(person, role, d, v)
                    except:
                        pass
        else:
            print(form.errors)

    return mr1(request, p,r,j)


def smrom(request):  # Доступность
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        if form.is_valid():
            for k, v in request.POST.items():

                if '.' in k:
                    p, r, j, d = k.split('.')

                    try:
                        person = UserProfile.objects.get(id=p)
                        role = Role.objects.get(id=r)
                        tr(person, role, d, v)
                    except:
                        pass
        else:
            print(form.errors)

    return mrom(request)  # s


def mjr(request, p, r, j):  # максимальна доступность одного ресурса и Остаточная доступность
    moon12 = moon()
    dif14 = []
    dif15 = []

    role = Role.objects.get(id=r)
    people_rr = people_of_rr(role)
    people_rv = people_of_rv(role)

    for person in people_rr:
        dif = pr_isfree_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {"link": f"{person.id}.{r}.0.{da.year}-{da.month}-15",

                         "title": dif[i]}  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    for person in people_rr:
        dif = pr_dif_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {"link": f"{person.id}.{r}.0.{da.year}-{da.month}-15",

                         "title": dif[i]}  # 9898
            da = inc(da)
        dif15.append([person.fio] + dif100)  ######################

    moon12["dif14"] = dif14

    moon12["dif15"] = dif15
    moon12["r"] = r
    moon12["j"] = j
    moon12["p"] = p
    moon12["role"] = role

    return render(request, 'mjr.html', moon12)


def mr2(request, p, r, j):  # максимальна доступность одного ресурса и Остаточная доступность
    moon12 = moon()
    dif14 = []
    dif15 = []

    role = Role.objects.get(id=r)
    people_rr = people_of_rr(role)

    for person in people_rr:
        dif = pr_isfree_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {"link": f"{person.id}.0.0.{da.year}-{da.month}-15",
                         "up": up(1, 2),
                         "title": dif[i]}  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################

    for person in people_rr:
        dif = pr_dif_(person, role)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {"link": f"{person.id}.0.0.{da.year}-{da.month}-15",

                         "title": dif[i]}  # 9898
            da = inc(da)
        dif15.append([person.fio] + dif100)  ######################

    moon12["dif14"] = dif14

    moon12["dif15"] = dif15
    moon12["r"] = r
    moon12["role"] = role

    return render(request, 'mr2.html', moon12)


def mr1(request, p, r, j):  # максимальна доступность одного ресурса и Остаточная доступность
    moon12 = moon()
    dif14 = []
    dif15 = []
    print(p,r,j)
    role = Role.objects.get(id=r)
    people_rr = people_of_rr(role)
    people_rv = people_of_rv(role)

    for person in people_rr:
        dif = pr_isfree_(person, role)
        is100 = p_101(person)

        dif100 = [0] * 12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i] = {"link": f"{person.id}.{role.id}.0.{da.year}-{da.month}-15",
                         "fire": is100[i],
                         "title": dif[i]}  # 9898
            da = inc(da)
        dif14.append([person.fio] + dif100)  ######################


    moon12["dif14"] = dif14

    moon12["dif15"] = dif15
    moon12["r"] = r
    moon12["role"] = role

    return render(request, 'mr1.html', moon12)


#
def mrom(request):  # Максимальная доступнасть по всем ресурсам
    moon12 = moon();
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
        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)
        px = {"val": role.title, "r": role.id}  #######################
        for person in people_rr:
            is100 = p_101(person)

            dif2 = [{"val": person.fio}] + [0] * 12
            dif = [person.fio] + pr_isfree_(person, role)
            d = date.today().replace(day=15)
            for i in range(12):

                if arr[person.id][role.id][i] > 100:
                    color = "pink"
                else:
                    color = "white"

                dif2[i + 1] = {
                    "link": f"{person.id}.{role.id}.0.{d.year}-{d.month}-15",
                    "color": color,
                    "val": dif[i + 1],
                    "fire": is100[i]}
                d = inc(d)

            dif14.append([px] + dif2)  ######################
            px = -1  ##################################

    moon12["dif14"] = dif14  ########################################

    return render(request, 'mrom.html', moon12)


#
def mro(request):  # Остаточная доступость по всем ресурсам
    moon12 = moon();
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()
    for role in roles:
        p9 = role.title
        people_rr = people_of_rr(role)
        people_rv = people_of_rv(role)
        px = role.title
        for person in people_rr:
            dif = [person.fio] + diffx(person, role)
            dif14.append([px] + dif)
            px = -1

    moon12["dif14"] = dif14

    return render(request, 'mro.html', moon12)


#

def mon_bar():
    dat = []
    d = date.today().replace(day=15)
    for i in range(12):
        dat.append({"year": d.year, "month": d.month})
        d = inc(d)

    return dat


def inc(d):
    y, m = d.year, d.month
    m += 1
    if m > 12:
        m = 1
        y += 1
    return date(y, m, 15)


################################################

def inc_n(d, n):
    for i in range(n):
        d = inc(d)
    return d


def tr(person, role, m, l):  # Доступность
    try:
        instance = Less.objects.get(person=person, role=role, start_date=m)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Less.objects.create(person=person, role=role, start_date=m, load=l)


def tjTask(p, r, j, d, l):  # Загрузка
    try:
        instance = Task.objects.get(person=p, project=j, role=r, month=d)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Task.objects.create(person=p, role=r, project=j, month=d, load=l)


def tjLoad(person, role, project, m, v):  # Потребность
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None

    if instance:
        instance.load = float(v)
        instance.save()

    else:
        instance = Load.objects.create(project=project, role=role, month=m, load=v)


def s1(request):
    p = 0
    r = 0
    j = 0
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            for k, v in request.POST.items():
                html = request.POST.get('html')
                if '.' in k:
                    p, r, j, d = k.split('.')
                    try:
                        project = Project.objects.get(id=j)
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)
                        tjTask(person, role, project, d, v)  ##################################
                    except:
                        pass
        else:
            print(form.errors)

    return eval(f"{html}(request,{p},{r},{j})")


def s2(request):
    p = 0
    j = 0
    r = 0
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            for k, v in request.POST.items():
                html = request.POST.get('html')
                if '.' in k:
                    p, r, j, d = k.split('.')

                    try:
                        person = None
                        role = Role.objects.get(id=r)
                        project = Project.objects.get(id=j)
                        tjLoad(person, role, project, d, v)
                    except:
                        pass
        else:
            print(form.errors)
    return eval(f"{html}(request,{p},{r},{j})")


def sj(request):
    j = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k, v in request.POST.items():
                sid = request.POST.get('id')
                j = int(sid)
                project = Project.objects.get(id=j)

                if '.' in k:
                    r, d = k.split('.')
                    role = Role.objects.get(id=r)
                    person = None
                    try:

                        tjLoad(person, role, project, d, v)


                    except:
                        pass
        else:
            print(form.errors)

        return aj(request, j)  #


def smj(request):
    p=-1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k, v in request.POST.items():
                sid = request.POST.get('id')
                j = int(sid)
                project = Project.objects.get(id=j)

                if '.' in k:
                    r, d = k.split('.')
                    role = Role.objects.get(id=r)
                    person = None
                    try:

                        tjLoad(person, role, project, d, v)

                    except:
                        pass
        else:
            print(form.errors)

        return mmj(request,p,r ,j)


def prjlist(request):  # все проекты (портфель)
    dmin = date.today()
    dmin = dmin.replace(day=15)
    dmax = inc_n(dmin, 11)
    moon12 = moon()
    projects = Project.objects.all().order_by('general', 'start_date')

    data = []
    for p in projects:
        data.append(pref(p) + [dif(p.start_date, p.end_date)] + mon_bool(dmin, dmax, p.start_date, p.end_date))

    moon12["matrix"] = data

    return render(request, 'prjlist.html', moon12)


def dif(d1, d2):
    return (d2.year - d1.year) * 12 + d2.month - d1.month + 1


def mon_bool(dmin, dmax, dstart, dend):
    L = []
    d = dmin.replace(day=15)
    d2 = dmax.replace(day=15)
    d3 = dstart.replace(day=15)
    d4 = dend.replace(day=15)
    while d <= d2:
        b = (d3 <= d <= d4)
        L.append(b)
        d = inc(d)
    return L


def pref(p):
    L = []
    L.append(p.general.fio)

    L.append({"title": p.title, "link": p.id})  # 989898

    L.append(p.start_date)
    L.append(p.end_date)
    return L


