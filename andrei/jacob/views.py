from django.shortcuts import render,redirect
from .models import Project, UserProfile, Load, Role, Task
import datetime,math

from django.forms import Form
def index(request):
    return render(request, 'index.html')

def people(request):
    people = UserProfile.objects.all()
    return render(request, 'people.html', {'people': people})

def tasks(request):
    form = None
    return render(request, 'tasks.html',{form:form})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
def load(request, id):
    project = Project.objects.get(id=id)
    d1 = project.start_date
    d2 = project.end_date
    month_tuples = ym_tuples(d1,d2)
    items_by_role_and_month = load_role_month(id)
    months = ym2mm(month_tuples)
    # Create a list of roles and their associated items for each month
    data = []
    for role, items_for_role in items_by_role_and_month.items():
        row = [role]
        for y,m in month_tuples:
            month = datetime.date(y,m,15)
            item = items_for_role.get(month)
            if item:
                row.append(item.load)
            else:
                row.append(0)
        data.append(row)

    # Pass the data to the template
    context = {'data': data, 'months': months,
               'd1':d1,'d2':d2,"project_id":id,
               'project':project, 'month_tuples': month_tuples}
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
            dat=[]

            dat.append(r)
            dat.append(p.user.last_name)
            n = 0
            for m in months:
                try:
                    t = {'load':tt[p][m],'link':f"{id}/{p.id}/{m.year}/{m.month}"}
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
               'd1':d1,'d2':d2,
               'project':project, 'month_tuples': month_tuples}
    return render(request, 'resp.html', context)


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

def load_role_month(prj):
    items = {}
    L = Load.objects.filter(project=prj).order_by('role', 'month')
    for l in L:
        m = l.month
        r = l.role

        if r not in items:
            items[r] = {}

        # Add the item to the dictionary for this role and month
        items[r][m] = l

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
    roles = Role.objects.all()
    for r in roles:
        users = UserProfile.objects.filter(id__in=people, role=r)
        L[r] = users

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
            ymtx = ymt(id)
            for k,v in request.POST.items():
                print(k,v)
                if '.' in k:
                    ki,kj=k.split('.')
                    ii = int(ki)-2
                    jj = int(kj)-1
                    y,m = ymtx[ii]
                    obj,created = Load.objects.update_or_create(
                        role=roles[jj],
                        project=project,
                        month=f"{y}-{m}-15",
                        load = int(v)
                    )
                    print(f"{y}-{m}-15",ii,jj,created,obj)
        else:
            print(form.errors)

    return redirect("load",id)
