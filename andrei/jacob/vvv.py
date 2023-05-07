from .forms import EntryForm
from django.shortcuts import render
from .models import Role,Project,Load,UserProfile,Task,Less

def frames40(request):#������������ ���� �������� � ���� ��������
    return render(request, 'frames40.html')

import datetime
def correct(data,l,n):
    d1 = datetime.date.today()
    dn = data[n]
    for i in range(12):
        if d1==l.start_date:
            dn[i+3]=l.load
        d1 = inc(d1)
    return data

def mon_bar():
    dat = []
    d = date.today().replace(day=15)
    for i in range(12):
        dat.append({"year":d.year,"month":d.month})
        d = inc(d)

    return dat
def inc(d):
    y,m = d.year,d.month
    m += 1
    if m > 12:
        m = 1
        y += 1
    return datetime.date(y,m,15)

def ostr(request,id,r):
    project = Project.objects.get(id=id)
    role = Role.objects.get(id=r)
    people = UserProfile.objects.filter(role=r)
    t12 = ['Фамилия','Имя']+mon_bar()
    data = [([p.user.last_name,p.user.first_name]+[1]*12) for p in people]
    n = 0
    for p in people:
        less = Less.objects.all().filter(person = p)
        for l in less:
            data = correct(data,l,n)

        tasks = Task.objects.all().filter(person=p)
        for t in tasks:
            data = correctOst(data,t,n)
        n+=1

    return render(request, 'ost.html', {'ost': people,"t12":t12,"data":data,"project":project,
                                          "role":role})
def res(request, id,r):
     project = Project.objects.get(id=id)
     experts = UserProfile.objects.all()
 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)

     a = {"link":f"{id}/{r}","title":role.title}
     dat1 = ['Потребность']+[0]*12
     dat3 = ['Аутсорс']+[0]*12
     dat5 = ['Дельта']+[0]*12
     dat2 = ['Поставка']+[0]*12
     dat4 = ['Вакансии']+[0]*12



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
         dat1[i + 1] = f"{num[i]}"  # = {dif[i]}")

         experts = UserProfile.objects.filter(role=r)
         for p in experts:
             try:
                 task = Task.objects.get(person=p, project=id, month=d)
                 sum[i] += task.load
             except:
                 pass
         d = inc(d)
         dat2[i + 1] = f"{sum[i]}"
         dif = num[i]-sum[i]
         dat5[i + 1] = f"{dif}"
     data.append(dat1)
     data.append(dat2)
     data.append(dat3)
     data.append(dat4)
     data.append(dat5)

     context = {'data': data,
              "data0":data0,"role":role,
                'project':project,  "experts":experts}
     return render(request, 'res.html', context)
def index(request):
    less = Less.objects.all()
    print(len(less))
    x = Less.objects.filter(person=6,start_date='2023-06-15')
    print(len(x))

    return render(request,'index.html',{})

def page_balances(request):
    p = None
    r = None
    roles="?"
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

            if p== None and r == None:

                return frames40(request)
            if p == None:

                return right(request,r.id)
            if r == None:
                # return left(request,p.id)
                pass
            return render(request, 'frames42.html',
                       {"pid": p.id, "rid": r.id, "project": project,"role":roles})
    else:
        form = EntryForm()
    return render(request, 't/page_balances.html',
                  {'form': form,"project":project,"role":roles})


def res01(request, id,r):
     project = Project.objects.get(id=id)
     d1 = project.start_date
 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)


     dat2 = [0]*12
     num = [0]*12
     d = date.today().replace(day=15)
     for i in range(12):
         try:
             L = Load.objects.get(project=id, role=r, month=d)
             num[i]=L.load
         except:
             num[i]=0
         dat2[i] = {"link":f"{d}","load":num[i]}
         d = inc(d)
     data.append(dat2)
     context = {'data': data,
               "data0":data0,"project_id":id,"r":r,"role":role,
                'project':project, }
     return render(request, 'res01.html', context)


def res10(request, id,r):

     project = Project.objects.get(id=id)

 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)

     n = 0
     d = date.today().replace(day=15)
     experts = UserProfile.objects.filter(role=r)
     for p in experts:
         sum = [0] * 12
         dat2 = [p] + [0] * 12
         for i in range(12):
             try:
                 task = Task.objects.get(person = p,project=id, month=d)
                 sum[i]=task.load
             except:
                 pass
             dat2[i+1] = {"link": f"{p.id}.{d}", "load": sum[i]}
             d = inc(d)
         data.append(dat2)

     context = {'data': data,
                 "data0":data0,"role":role,"project_id":id,"r":r,
                'project':project}
     return render(request, 'res10.html', context)



def correctOst(data,l,n):
    d1 = datetime.date.today()
    dn = data[n]
    for i in range(12):
        if inside(d1,l.month,l.month):
            dn[i+3]-=l.load
        d1 = inc(d1)
    return data

# def ostatok(request):
#     people = UserProfile.objects.all()
#     t12 = ['�������','���']+mon_bar()
#     data = [([p.role,p.user.last_name,p.user.first_name]+[1]*12) for p in people]
#     n = 0
#     for p in people:
#         less = Less.objects.all().filter(person = p)
#         for l in less:
#             data = correct(data,l,n)
#
#         tasks = Task.objects.all().filter(person=p)
#         for t in tasks:
#             data = correctOst(data,t,n)
#         n+=1
#
#     return render(request, 'ost.html', {'ost': people,"t12":t12,"data":data,"role":role,})

def inside(d,d1,d2):
    b = (d1.year,d1.month) <= (d.year,d.month) <= (d2.year,d2.month)

def frames42(request, pid, rid, project):  # ������������ ������� (������) � ������� (������)
        return render(request, 'frames42.html', {"pid": pid, "rid": rid, "project": project})

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


def projects(request):
    projects = Project.objects.all().order_by('start_date')
    dmin = date.today()
    dmin=dmin.replace(day=15)
    dmax = inc_n(dmin,12)
    tuples = ym_tuples(dmin,dmax)

    data = []
    for p in projects:
        mb = mon_bool(dmin,dmax,p.start_date,p.end_date)
        data.append(pref(p)+[dif(p.start_date,p.end_date)]+mon_bool(dmin,dmax,p.start_date,p.end_date))
    return render(request, 'prjlist.html', {'prjects': projects,"months":tuples,"matrix":data})
def otd_context(request):
    roles = Role.objects.all().order_by('id')
    people = UserProfile.objects.all()
    mss=t12ym()

    t12 = ['Роль'] + mss
    data = []
    data2 = []
    data3 = []
    d1 = date.today()
    for r in roles:
        dat = []
        dat2 = []
        dat3 = []
        num = [1] * 12
        sum = [0] * 12
        sum2 = [0] * 12

        dat.append({'title':r,'link':r.id})
        dat2.append({'title': r, 'link': r.id})
        dat3.append({'title': r, 'link': r.id})
        n = 0

        experts = UserProfile.objects.filter(role=r)
        for person in experts:
            less = Less.objects.filter(person = person).order_by('id')
            for l in less:

                d = d1
                for i in range(12):
                    if d==l.start_date:
                        num[i]=l.load

                    d = inc(d)
            for i in range(12):
                sum[i]+=num[i]
            i=0
            for m in mss:
                d = date(year=m['year'],month=m['month'],day=15)
                tasks = Task.objects.filter(person=person,month=d)

                for task in tasks:
                    t = task.load
                    sum2[i]+=t
                i+=1
            num = [1] * 12

        dat+=[sum[i] for i in range(12)]
        dat2 += [sum2[i] for i in range(12)]
        dat3 += [sum[i]-sum2[i] for i in range(12)]
        data.append(dat)
        data2.append(dat2)
        data3.append(dat3)
    context = {'data': data,'data2': data2,'data3': data3,
               't12': t12,}
    return context

def load(request, id):
    data0 = mon_bar()
    roles = Role.objects.all().order_by('id')
    project = Project.objects.get(id=id)
    d1 = project.start_date

    # Create a list of roles and their associated items for each month
    data = []

    for role in roles:
        row = [role]

        #for ms in mss:
        d = date.today().replace(day=15)
        for i in range(12):

            try:
                tt = Load.objects.get(project=project,role=role,month=d)
                t=tt.load
            except:
                t=0

            x = {"link": f"{role.id}.{d}", "load": t}
            row.append(x)
            d = inc(d)
        data.append(row)

    # Pass the data to the template
    context = {'data': data,'data0': data0,
               'd1':d1,"project_id":id,
               'project':project}

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

    dat2 = ['�����������']
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
#         dat.append('������')
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
#
#     month_tuples = ym_tuples(d1, d2)
#     items = load_role_month(id)
#     mss = ymts(id)  # str format
#     months = ym2mm(month_tuples)  # datetime format
#     experts = person_role(id)
#
#     N = len(months)
#     tt = task_prj_person_month(id, mss)

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
#         dat.append('�����������')
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
#         dat.append('������')
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
def updateORcreateLess(p, d, l):
    print(p,d,l,888)
    person = UserProfile.objects.get(id=p)
    try:
        instance = Less.objects.get(person=person, start_date=d)
    except:
        instance = None

    if instance:
        print(789)
        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one
        print(5,person,d,l)
        instance = Less.objects.create(person=person, start_date=d, load=l)
        print(6)

def updateORcreate(p, pj, d, l):
    print(159,p,pj,d,l)
    try:
        print(1)
        instance = Task.objects.get(person=p,project=pj, month=d)
    except Task.DoesNotExist:
        instance = None
        print(2)
    if instance:
        print(3)
        instance.load = l
        instance.save()
    else:
        print(4)
        # If the instance does not exist, create a new one
        instance = Task.objects.create(person=p, project=pj, month=d, load=l)
        print(5)


def updateORcreateL(project,role, m, l):
    print(878)
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except Load.DoesNotExist:
        instance = None

    if instance:
        instance.load = l
        instance.save()


    else:
        print(317)
        instance = Load.objects.create(project=project, role=role, month=m, load=l)
        print(318)

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
    d2 = datetime.date(year=y,month=m,day=15)
    return d2


def pref(p):
    L = []
    L.append(p.general.user.last_name)

    L.append({"title":p.title,"link":p.id})

    L.append(p.start_date)
    L.append(p.end_date)
    return L
from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
from .forms import LoadForm, CellForm
######################################################################


# views.py
from django.shortcuts import render, redirect
from .forms import UpdateFloatForm
from .models import Task
import datetime

from django.shortcuts import render
from .forms import TableCellForm, table_to_formset
def ajax0(request):
    print(1024)
    id = 1
    r=1
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        if form.is_valid():
            id = int(request.POST.get('id'))
            project = Project.objects.get(id=id)
            for k,v in request.POST.items():
                print(k,v,500)
                if '.' in k:
                    print(567)
                    r,d = k.split('.')
                    l = float(v)
                    role = Role.objects.get(id=r)
                    updateORcreateL(project,role,d,l)
                    print(568)

        else:
            print(form.errors)

    return load(request,id)
def ajax(request):

    id = 1
    r=1
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        if form.is_valid():
            id = int(request.POST.get('id'))
            project = Project.objects.get(id=id)
            sr = int(request.POST.get('r'))
            r=int(sr)
            role = Role.objects.get(id=r)
            for d,v in request.POST.items():
                if '-' in d:
                    l = float(v)
                    updateORcreateL(project,role,d,l)


        else:
            print(form.errors)

    return res01(request,id,r)

def jax2(request):
    print(88)
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():

            sid = request.POST.get('id')
            id = int(sid)
            sr = request.POST.get('r')
            r = int(sr)
            project = Project.objects.get(id=id)

            for k,v in request.POST.items():
              if '.' in k:
                print(995,k)
                p,d=k.split('.')
                print(994,p,d)
                try:
                    print(78,p,d)
                    person=UserProfile.objects.get(id=p)
                    l = float(v)
                    updateORcreate(person,project,d,l)
                except:
                    pass
        else:
            print(form.errors)

    return redirect("res10",id,r)
def jax3(request):
    print(88)
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sr = request.POST.get('r')
            r = int(sr)
            for k,v in request.POST.items():
              if '.' in k:
                p,d=k.split('.')
                try:
                    l = float(v)
                    updateORcreateLess(p,d,l)
                except:
                    pass
        else:
            print(form.errors)

    return myotd1(request,r)

def people(request):
    people = UserProfile.objects.all().order_by("role")
    t12 = ['����','�������','���']+t12ym()
    data = [([p.role,p.user.last_name,p.user.first_name]+[1]*12) for p in people]
    data1 = [([0,0,0]+[1]*12) for p in people]
    n = 0
    for p in people:
        less = Less.objects.all().filter(person = p)
        for l in less:
            data = correct(data,l,n)
        n+=1

    k = 0
    for p in people:
        d = datetime.now().date()
        sum = 0
        for i in range(12):
            t = tasks(p.id,d)
            d = inc(d)
            if(t>0):

                data[k][i+3]={"d":data[k][i+3],"t":t}

        k+=1
    return render(request, 'people.html', {'people': people,"t12":t12,"data":data})

from datetime import date
from .models import Role


from django.shortcuts import render
from .models import Load, Role, Project, UserProfile, Less, Task

def myotd1(request,r):
    context = myotd(request,r)
    return render(request, 'myotd1.html',context)

def myotd2(request,r):
    print(88)
    context = myotd(request,r)
    return render(request, 'myotd2.html',context)

def myotd3(request,r):
    print(77)
    context = myotd(request,r)
    return render(request, 'myotd3.html',context)

def myotd(request,r):
    mss=t12ym()

    t12 = ['Ресурс'] + mss
    data = []
    data1 = []
    data2=[]
    data3=[]
    num = [1] * 12
    sum = [0] * 12
    sum2 = [0] * 12

    d1 = date.today().replace(day=15)
    role = Role.objects.get(id=r)
    experts = UserProfile.objects.filter(role=r)
    mss = t12ym()
    for person in experts:
        user = UserProfile.objects.get(id=person.id).user
        dat1=[]
        dat2 = [{"title": user.last_name, "link": person.id}]
        dat3 = [{"title": user.last_name, "link": person.id}]

        num = [1] * 12
        sum = [0] * 12
        sum2 = [0] * 12

        dat1 = [1]*12
        d1 = date.today().replace(day=15)
        for i in range(12):
            dat1[i] = {"link":f"{person.id}.{d1}","load":1}
            try:
                print(314,person,d1)
                less = Less.objects.filter(person=person,start_date=d1)
                for l in less:
                    print(315)
                    num[i] = l.load
                    print(316)
                    dat1[i] = {"link":f"{person.id}.{d1}","load":l.load}
                    print(317)
            except:
                pass
            d1 = inc(d1)
        for i in range(12):
            sum[i] += num[i]
        i = 0
        d = date.today().replace(day=15)
        for m in mss:

            tasks = Task.objects.filter(person=person, month=d)

            for task in tasks:
                t = task.load
                sum2[i] += t
            i += 1
            d = inc(d)
            num = [1] * 12

        dat1 = [{"title":user.last_name,"link":person.id}]+dat1
        dat2 += [sum2[i] for i in range(12)]
        dat3 += [sum[i]-sum2[i] for i in range(12)]

        data1.append(dat1)
        data2.append(dat2)
        data3.append(dat3)
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3, "r":r,
               't12': t12,'role_id':r,'role':role,}
    print("hello")
    return context




def left(request):
    return render(request, 'frames2left.html')

def right(request):
    return render(request, 'frames2right.html')

    # return render(request, 'frames1res1.html',context)

def res11(request,r):
    return render(request, 'frames1res1.html', {"r":r})



def details(request):
    return render(request, 'details.html')

def frames1prj(request):
    return render(request, 'frames1prj.html')
def frames1res(request):
    return render(request, 'frames1res.html')

def otdlist(request,i):
    context = otd_context(request)
    return render(request,f"otdlist{i}.html",context)


def prjlist(request):
    return projects(request)


def t12ym():
   L = []
   d1 = date.today()
   for i in range(12):
       L.append({"year":d1.year,"month":d1.month})
       d1 = inc(d1)

   return L

def inside(d,d1,d2):
    b = (d1.year,d1.month) <= (d.year,d.month) <= (d2.year,d2.month)

    return b

def correct(data,l,n):
    d1 = date.today()
    dn = data[n]
    for i in range(12):
        if d1==l.start_date:
            dn[i+3]=l.load
        d1 = inc(d1)
    return data


def inc_n(d,n):
    for i in range(n):
        d = inc(d)
    return d

def tasks(person):
    d1 = datetime.date.today().replace(day=15)

    ms = [0]*12
    d = d1
    for i in range(12):
        tasks = Task.objects.all().filter(person=person,month = d)
        for t in tasks:
            ms[i] += t.load
        d = inc(d)

    return ms

def dost(person):
    d1 = datetime.date.today().replace(day=15)
    d2 = inc_n(d1,12)
    ms = [1]*12
    d = d1
    i = 0
    while d <= d2:
        less = Less.objects.filter(person=person).order_by("id")
        for l in less:
            if d==l.start_date:
                ms[i] = l.load
        i+=1
        d = inc(d)
    return ms


def ost(person,ms):
    return dost(person,ms)-tasks(person,ms)


def one2prj(request):
    people = UserProfile.objects.all().order_by('role', 'user')
    projects = Project.objects.all().order_by('start_date')
    one = []
    for person in people:
        one.append(person.user.last_name)
        for project in projects:
            ps = list(project.people.all())
            if person in ps:
                one.append(1)
            else:
                one.append(0)

    return render(request,"one2prj.html",{'people':people, 'projects':projects, "one":one},)

def one2role(request):
    roles = Role.objects.all()
    people = UserProfile.objects.all().order_by('role','user')

    return render(request,"one2role.html",{'roles':roles,'people':people},)

from django.shortcuts import render
from .forms import EntryForm
from .models import Project,Role




def left(request,pid):#���������� ������
    return render(request, 'frames2left.html',{'id':pid})

def right(request,rid):#���������� ������
    return render(request, 'frames2right.html',{'id':rid})
def entry(request):#������� ����
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

            if p== None and r == None:
                return frames40(request)
            if p == None:
                return res11(request,r.id)
            if r == None:
                return left(request,p.id)
            return frames42(request,p.id,r.id,project)
    else:
        form = EntryForm()
    return render(request, 'entry.html', {'form': form,"project":project})
