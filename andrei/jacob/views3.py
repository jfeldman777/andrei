from .models import Project, UserProfile, Load, Role, Task
import datetime,math

from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
#################################################
def load(request, id):
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
        row = [role]
        for ms in mss:
            try:
                load = items[role][ms]
                t=load
            except:
                t=0
            x = {"link":f"{role.id}.{ms}","load":t}
            row.append(x)
        data.append(row)

    # Pass the data to the template
    context = {'data': data,
               'd1':d1,'d2':d2,"project_id":id, 'month_tuples': month_tuples,
               'project':project}
    return render(request, 'load3.html', context)

def res(request, id):
    project = Project.objects.get(id=id)
    d1 = project.start_date
    d2 = project.end_date
    month_tuples = ym_tuples(d1,d2)
    items = load_role_month(id)

    months = ym2mm(month_tuples)
    experts = person_role(id)
##################################
    data = []
    tt = task_prj_person_month(id, months)
    roles = Role.objects.all().order_by('id')
    N = len(month_tuples)
    for r in roles:
        dat = [r]+[0]*N
        num = [0]*N
        sum = [0]*N
        n = 0
        for y,m in month_tuples:
            month = datetime.date(y,m,15)
            try:
                item = items[r][month]
                num[n] = item.load
            except:
                num[n] = 0

            n+=1
            for i in range(N):
                dat[i+1]=num[i]
        else:

            for p in experts[r]:
                n = 0
                for m in months:
                    try:
                        sum[n]+=tt[p][m]
                    except:
                        pass
                    n+=1
            dif = [round(num[i]-sum[i],2) for i in range(n)]
            for i in range(n):
                dat[i+1]=(f"{num[i]} - {sum[i]} = {dif[i]}")
        data.append(dat)



    context = {'data': data, 'months': months,
               'd1':d1,'d2':d2,
               'project':project, 'month_tuples': month_tuples, "experts":experts}
    return render(request, 'res.html', context)

def resp(request, id):
    # Get all the items for the given ID and sort by role and month
    project = Project.objects.get(id=id)
    experts = {}
    roles = Role.objects.all().order_by('id')

    d1 = project.start_date
    d2 = project.end_date
    month_tuples = ym_tuples(d1,d2)
    items = load_role_month(id)
    months = ym2mm(month_tuples)
    # Create a dictionary to store the items by role and month
    experts = person_role(id)
    N = len(months)
    tt = task_prj_person_month(id, months)
    data = []

    iy = -1

    for r in roles:
        dat = []
        num = [0]*N
        sum = [0]*N
        dat.append(r)
        dat.append('ПОТРЕБНОСТЬ')
        n = 0
        for y,m in month_tuples:
            month = datetime.date(y,m,15)
            try:
                item = items[r][month]
                dat.append(item.load)
                num[n]=item.load
            except:
                dat.append(0)
                num.append(0)
            n+=1
        data.append(dat)
        for p in experts[r]:
            iy+=1
            dat=[]

            dat.append(r)
            dat.append(p.user.last_name)
            n = 0
            ix=-1
            for m in months:
                ix+=1
                try:
                    t = {'load':tt[p][m],'link':f"{ix}.{p.id}"}
                    dat.append(t)
                    sum[n]+=tt[p][m]
                except:
                    dat.append(0)
                n+=1

            data.append(dat)

        dif = [round(num[i]-sum[i],2) for i in range(N)  ]
        dat = []
        dat.append(r)
        dat.append('ДЕЛЬТА')
        k = 0
        for m in months:
            dat.append(dif[k])
            k+=1
        data.append(dat)
    context = {'data': data, 'months': months,
               'd1':d1,'d2':d2,"project_id":id,
               'project':project, 'month_tuples': month_tuples}
    return render(request, 'resp.html', context)

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
def person_sorted(prj):
    people = Project.objects.get(id=prj).people.all()
    L = []
    roles = Role.objects.all().order_by('id')
    for r in roles:
        users = list(UserProfile.objects.filter(id__in=people, role=r).order_by('user'))
        L+=users
    return L
def ajax(request):
    id = 1
    roles = list(Role.objects.all().order_by('id'))
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #id = form.cleaned_data["id"]
            id = int(request.POST.get('id'))
            project = Project.objects.get(id=id)
            for k,v in request.POST.items():
                if '.' in k:
                    ki,m=k.split('.')
                    ri = int(ki)
                    role = Role.objects.get(id=ri)
                    l = float(v)
                    updateORcreateL(project,role,m,l)
        else:
            print(form.errors)

    return redirect("load",id)

def ajax2(request):
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sid = request.POST.get('id')
            id = int(sid)
            project = Project.objects.get(id=id)
            people = person_sorted(id)
            ymtx = ymt(id)
            for k,v in request.POST.items():
                if '.' in k:
                    ki,kj=k.split('.')
                    ix = int(ki)
                    iy = int(kj)
                    role=Role.objects.get(id=ix)
                    y,m = ymtx[iy]
                    updateORcreate(role,project,f"{y}-{m}-15",float(v))
        else:
            print(form.errors)

    return redirect("resp",id)

def updateORcreate(p, pj, m, l):
    try:
        instance = Task.objects.get(person=p,project=pj, month=m)
    except Task.DoesNotExist:
        instance = None

    if instance:
        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one
        instance = Task.objects.create(person=p, project=pj, month=m, load=l)

def updateORcreateL(project,role, m, l):

    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except Load.DoesNotExist:
        instance = None

    if instance:
        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one
        instance = Load.objects.create(project=project, role=role, month=m, load=l)