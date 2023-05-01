from .models import Project, UserProfile, Load, Role, Task
import datetime

from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
#################################################

def inc_n(d,n):
    for i in range(n):
        d = inc(d)
    return d

def mon_bar():
    dat = []
    d = datetime.date.today().replace(day=15)
    for i in range(12):
        dat.append({"year":d.year,"month":d.month})
        d = inc(d)

    return dat


def projects(request):
    projects = Project.objects.all().order_by('start_date')
    dmin = datetime.date.today().replace(day=15)
    dmax = inc_n(dmin,12)
    tuples = ym_tuples(dmin,dmax)

    data = []
    for p in projects:
        mb = mon_bool(dmin,dmax,p.start_date,p.end_date)
        data.append(pref(p)+[dif(p.start_date,p.end_date)]+mon_bool(dmin,dmax,p.start_date,p.end_date))
    return render(request, 'prjlist.html', {'projects': projects,"months":tuples,"matrix":data})


def load(request, id):
    data0 = mon_bar()
    roles = Role.objects.all().order_by('id')
    project = Project.objects.get(id=id)
    d1 = project.start_date
    d2 = project.end_date
    month_tuples = ym_tuples(d1, d2)
    items = load_role_month(id)
    mss = ymts(id)
    # Create a list of roles and their associated items for each month
    data = []
    for role in roles:
        row = [{"link":f"{id}/{role.id}","title":role}]
        print(row)
        #for ms in mss:
        d = datetime.date.today().replace(day=15)
        for i in range(12):
            try:
                tt = Load.objects.get(project=project,role=role,month=d)
                t=tt.load
            except:
                t=0
            x = {"link":f"{role.id}.{d}","load":t}
            row.append(x)
            d = inc(d)
        data.append(row)

    # Pass the data to the template
    context = {'data': data,'data0': data0,
               'd1':d1,'d2':d2,"project_id":id, 'month_tuples': month_tuples,
               'project':project}
    print(567,role)
    return render(request, 'load.html', context)

def mytask(request, id):
    person = UserProfile.objects.get(id=id)
    tasks = Task.objects.filter(person=id)
    d1 = datetime.date.today().replace(day=15)
    dat1=mon_bar()

    data = []
    projects = Project.objects.all()
    for project in projects:
        dat = [project]
        d = datetime.date.today().replace(day=15)
        for i in range(12):
            try:
                task = Task.objects.get(person=id, project=project, month=d)
                # print(person, project, d, task)
                t = task.load
            except:
                t=0

            dat.append(t)
            d = inc(d)
        data.append(dat)

    context = {'dat1': dat1,'data':data,
              "person":person
              }
    return render(request, 'mytask.html', context)

def res_jr(request, prj,r):
    project = Project.objects.get(id=prj)
    role = Role.objects.get(id=r)
    d1 = datetime.date.today().replace(day=15)
    experts = UserProfile.objects.filter(role=r)
    N = 12
    num = [0] * N
    n=0


    dat1=mon_bar()
    # print(99,dat1)
    dat2 = ['ПОТРЕБНОСТЬ']
    d = datetime.date.today().replace(day=15)
    for n in range(12):
        try:
            task = Load.objects.get(project=prj,month=d)
            t = task.load
        except:
            t = 0
        num[n]=t
        d = inc(d)
        dat2.append(t)
    data=[]
    n=0
    for e in experts:
        dat = [e.user.last_name]
        d = datetime.date.today().replace(day=15)
        for n in range(12):
            try:
                task = Task.objects.get(person=e,month=d)
                load = task.load
            except:
                load = 0

            x = {"link": f"{e.id}.{d}.{r}", "load": load}
            dat.append(x)

            d = inc(d)
    data.append(dat)
    context = {'data': data,"dat1":dat1,"dat2":dat2,"role":role,"project":project}

    return render(request, 'res_jr.html', context)

def res(request, id,r):

     project = Project.objects.get(id=id)


     experts =  person_role(id)
 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)

     a = {"link":f"{id}/{r}","title":role.title}
     dat1 = [a,'Потребность']+[0]*12
     dat3 = [a,'Аутсорс']+[0]*12
     dat5 = [a,'Дельта']+[0]*12
     dat2 = [a,'Поставка']+[0]*12
     dat4 = [a,'Вакансии']+[0]*12

     # print(id,load)

     num = [0]*12
     sum = [0]*12
     n = 0
     d = datetime.date.today().replace(day=15)

     for i in range(12):
         try:
             L = Load.objects.get(project=id, role=r, month=d)
             num[i] = L.load
         except:
             num[i] = 0
         dat1[i + 2] = f"{num[i]}"  # = {dif[i]}")

         experts = UserProfile.objects.filter(role=r)
         for p in experts:
             try:
                 task = Task.objects.get(person=p, project=id, month=d)
                 sum[i] += task.load
             except:
                 pass
         d = inc(d)
         dat2[i + 2] = f"{sum[i]}"




         dif = round(num[i]-sum[i],2)
         dat5[i + 2] = f"{dif}"
     data.append(dat1)
     data.append(dat2)
     data.append(dat3)
     data.append(dat4)
     data.append(dat5)



     context = {'data': data,
              "data0":data0,
                'project':project,  "experts":experts}
     return render(request, 'res.html', context)
#
# def res_all(request):
#     roles = Role.objects.all().order_by('id')
#     d1 = datetime.now().date()
#     d2 = inc_n(d1,12)
#
#     month_tuples = ym_tuples(d1, d2)
#     # items = load_role_month(id)
#     # mss = ymts(id)  # str format
#     # months = ym2mm(month_tuples)  # datetime format
#     # experts = person_role(id)
#
#     experts = UserProfile.objects.all()
#
#     # N = len(months)
#     # print(tt)
#     # print(mss)
#
#     data = []
#     for e in experts:
#         dat = []
#         num = [0] * 12
#         sum = [0] * 12
#         dat.append(e.user.last_name)
#         n = 0
#
#
#     tasks = Task.objects.filter(person=e)
#     for t in tasks:
#
#
#
#         for ms in mss:
#             try:
#                 load = items[r][ms]
#                 dat.append(load)
#                 num[n] = load
#             except:
#                 dat.append(0)
#                 num.append(0)
#             n += 1
#         data.append(dat)
#         for p in experts[r]:
#             dat = []
#             dat.append(r)
#             dat.append(p.user.last_name)
#             n = 0
#             for ms in mss:
#                 try:
#                     t = {'load': tt[p][ms], 'link': f"{p.id}.{ms}"}
#                     dat.append(t)
#                     sum[n] += tt[p][ms]
#                 except:
#                     dat.append(0)
#                 n += 1
#
#             data.append(dat)
#
#         dif = [round(num[i] - sum[i], 2) for i in range(N)]
#         dat = []
#         dat.append(r)
#         dat.append('ДЕЛЬТА')
#         k = 0
#         for m in months:
#             dat.append(dif[k])
#             k += 1
#         data.append(dat)
#     context = {'data': data, 'months': months,
#                'd1': d1, 'd2': d2, "project_id": id,
#                'project': project, 'month_tuples': month_tuples}
#     return render(request, 'resp.html', context)
#
# def resp(request, id):
#     project = Project.objects.get(id=id)
#     roles = Role.objects.all().order_by('id')
#     d1 = project.start_date
#     d2 = project.end_date
#     month_tuples = ym_tuples(d1, d2)
#     items = load_role_month(id)
#     mss = ymts(id)  # str format
#     months = ym2mm(month_tuples)  # datetime format
#     experts = person_role(id)
#
#     N = len(months)
#     tt = task_prj_person_month(id, mss)
#     print(tt)
#     print(mss)
#
#     data = []
#
#     iy = -1
#
#     for r in roles:
#         dat = []
#         num = [0]*N
#         sum = [0]*N
#         dat.append(r)
#         dat.append('ПОТРЕБНОСТЬ')
#         n = 0
#
#
#         for ms in mss:
#             try:
#                 load = items[r][ms]
#                 dat.append(load)
#                 num[n]=load
#             except:
#                 dat.append(0)
#                 num.append(0)
#             n+=1
#         data.append(dat)
#         for p in experts[r]:
#             dat=[]
#             dat.append(r)
#             dat.append(p.user.last_name)
#             n = 0
#             for ms in mss:
#                 try:
#                     t = {'load':tt[p][ms],'link':f"{p.id}.{ms}"}
#                     dat.append(t)
#                     sum[n]+=tt[p][ms]
#                 except:
#                     dat.append(0)
#                 n+=1
#
#             data.append(dat)
#
#         dif = [round(num[i]-sum[i],2) for i in range(N)  ]
#         dat = []
#         dat.append(r)
#         dat.append('ДЕЛЬТА')
#         k = 0
#         for m in months:
#             dat.append(dif[k])
#             k+=1
#         data.append(dat)
#     context = {'data': data, 'months': months,
#                'd1':d1,'d2':d2,"project_id":id,
#                'project':project, 'month_tuples': month_tuples}
#     return render(request, 'resp.html', context)

def ymts(id):
    tt = ymt(id)
    ls = [f"{y}-{m}-15" for y,m in tt]
    return ls
def ymt(id):
    project = Project.objects.get(id=id)
    d1 = project.start_date
    d2 = project.end_date
    return ym_tuples(d1,d2)
def ym_tuples(d1,d2):
    y1, m1 = d1.year, d1.month
    y2, m2 = d2.year, d2.month
    tuples = []
    while (y1, m1) <= (y2, m2):
        tuples.append((y1, m1))
        m1 += 1
        if m1 > 12:
            m1 = 1
            y1 += 1
    return tuples

def d2s(d):
    y = d.year
    m = d.month
    s = f"{y}-{m}-15"
    return s


def res_j(person,prj,p):
    items = {}
    L = Task.objects.filter(project=prj, person = p)
    for l in L:
        m = l.month
        r = l.role
        s = d2s(m)

        # Add the item to the dictionary for this role and month
        items[r][s] = l.load

    return items
def load_role_month(prj):
    items = {}
    L = Load.objects.filter(project=prj).order_by('role', 'month')
    for l in L:
        m = l.month
        r = l.role
        s = d2s(m)

        if r not in items:
            items[r] = {}

        # Add the item to the dictionary for this role and month
        items[r][s] = l.load
    print(items)
    return  items

def ym2mm(tuples):
    mm = []
    for t in tuples:
        y,m = t
        mx = datetime.date(y,m,15)
        mm.append(mx)
    return mm

def task_prj_person_month(prj,ms):
        people = Project.objects.get(id=prj).people.all()
        res = {}
        for p in people:
            res[p]={}
            print(999,ms)
            for m in ms:
                try:
                    t = Task.objects.get(project=prj,person = p,month = m)
                    res[p][m]=t.load
                except:
                    res[p][m] = 0

        return res


def person_role(prj):
    people = Project.objects.get(id=prj).people.all()
    L = {}
    roles = Role.objects.all().order_by('id')
    for r in roles:
        users = UserProfile.objects.filter(id__in=people, role=r).order_by('user')
        L[r] = users
    return L
# def person_sorted(prj):
#     people = Project.objects.get(id=prj).people.all()
#     L = []
#     roles = Role.objects.all().order_by('id')
#     for r in roles:
#         users = list(UserProfile.objects.filter(id__in=people, role=r).order_by('user'))
#         L+=users
#     return L


def updateORcreate(p, pj, m, l):
    print(777)

    try:
        instance = Task.objects.get(person=p,project=pj, month=m)
    except Task.DoesNotExist:
        instance = None

    if instance:
        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one
        project = Project.objects.get(id=pj)
        instance = Task.objects.create(person=p, project=project, month=m, load=l)

def updateORcreateL(p,r, m, l):
    print(666,p,r, m, l)
    role = Role.objects.get(id=r)
    project = Project.objects.get(id=p)
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
        print(667)
    except Load.DoesNotExist:
        instance = None

    if instance:
        instance.load = l
        instance.save()

        print(669)
    else:
        # If the instance does not exist, create a new one
        instance = Load.objects.create(project=project, role=role, month=m, load=l)
        print(699)

def dif(d1,d2):
    return (d2.year-d1.year)*12+d2.month-d1.month+1
def mon_bool(dmin,dmax,dstart,dend):
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

def inc(d):
    y,m = d.year,d.month
    m += 1
    if m > 12:
        m = 1
        y += 1
    return datetime.date(y,m,15)

def pref(p):
    L = []
    L.append(p.general.user.last_name)

    L.append({"title":p.title,"link":p.id})

    L.append(p.start_date)
    L.append(p.end_date)
    return L

def res01(request, id,r):
     project = Project.objects.get(id=id)
     d1 = project.start_date
 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)

     a = {"link":f"{id}.{r}","title":role.title}
     dat2 = [a]+[0]*12
     num = [0]*12
     d = datetime.date.today().replace(day=15)
     for i in range(12):
         try:
             L = Load.objects.get(project=id, role=r, month=d)
             num[i]=L.load
         except:
             num[i]=0
         dat2[i+1] = {"link":f"{d}","load":num[i]}
         d = inc(d)
     data.append(dat2)
     context = {'data': data,
               "data0":data0,"project_id":id,"r":r,
                'project':'Профиль загрузки (потребность)', }
     return render(request, 'res01.html', context)


def res10(request, id,r):

     project = Project.objects.get(id=id)

 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)

     a = {"link":f"{id}/{r}","title":role.title}

     dat2 = [a]+[0]*12
     sum = [0]*12
     n = 0
     d = datetime.date.today().replace(day=15)
     for i in range(12):
         experts = UserProfile.objects.filter(role=r)
         for p in experts:
             try:

                 task = Task.objects.get(person = p,project=id, month=d)
                 sum[i]+=task.load
                 print(88,task.load)
             except:
                 pass
         d = inc(d)
         dat2[i+1]=f"{sum[i]}"
     data.append(dat2)

     context = {'data': data,
                "data0":data0,
                'project':'Утвержденные загрузки (поставка)'}
     return render(request, 'res10.html', context)