from .models import Role,Project,Load,UserProfile,Task,Less
from .forms import EntryForm
from datetime import *
from django.shortcuts import render,redirect,reverse
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task

def test(request):
    person = UserProfile.objects.get(id=4)
    Less.objects.create(person=person,start_date='2023-12-15',load=2)
    return render(request,'a00.html')
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

            # if p== None and r == None:
            #     return a00(request)
            # if r==None:
            #     return a3(request,p.id)
            # if p==None:
            #     return a2(request,r.id)

            return ajr(request,p.id,r.id)

    form = EntryForm()
    return render(request,'alf.html', {'form': form})

def att(request):
    projects = Project.objects.all().order_by ('general')
    data = []
    for p in projects:
        x = {"project_id":p.id,
            "project":p.title,
        "name":p.general.fio}
        data.append(x)
    context = {"data":data}

    roles = Role.objects.all().order_by ('general')
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {"res_id":p.id,
            "title":p.title,
        "name":u.fio}
        data2.append(x)
    context["data2"]=data2

    return render(request,'att.html',context)

def a00(request):
    return render(request,'a00.html')
def zero(name):
        sum = [name]+[0]*12
        return sum

def diffx(person):
    projects = Project.objects.all()
    sum = [0]*12
    for project in projects:
        s = supply(project,person)
        for i in range(12):
            sum[i]+=s[i]
    ls = less(person)
    for i in range(12):
        ls[i]-=sum[i]

    return ls

def less(person):
    les = [1]*12
    d = date.today().replace(day=15)
    for i in range(12):
        L = list(Less.objects.filter(start_date=d,person=person))
        try:
            t = L[0].load
        except:
            t = 1
        d = inc(d)
        les[i]=t
    return les

def supply(project,person):
        sp=[0]*12
        d = date.today().replace(day=15)
        for i in range(12):
            L = list(Task.objects.filter(project=project,month=d,person=person))
            try:
                t = L[0].load
            except:
                t = 0
            d = inc(d)
            sp[i]=t
        return sp

def demand(project,role):
    dem = [0]*12
    d = date.today().replace(day=15)
    for i in range(12):
        L = list(Load.objects.filter(project=project,month=d,role=role))
        try:
            t = L[0].load
        except:
            t = 0
        d = inc(d)
        dem[i]=t
    return dem



def moon():
    y_data = []
    m_data = []
    d = date.today().replace(day=15)
    for i in range(12):
            y_data.append(d.year)
            m_data.append(d.month)
            d = inc(d)
    return {"yy":y_data,"mm":m_data}

def ajr(request,j,r):
    moon12 = moon();
    dem13 = []
    sup13e = []
    sup13 = []
    dif13 = []

    project = Project.objects.get(id=j)
    role = Role.objects.get(id=r)
    dem = demand(project,role)
    dem13.append(['Потребность']+dem)

    people = UserProfile.objects.filter(role = role)
    supp=[0]*12
    for person in people:

        sup = supply(project,person)
        sup2 = [0]*12

        d = date.today().replace(day=15)
        for i in range(12):
            sup2[i]={"link":f"{person.id}.{d.year}-{d.month}-15","val":sup[i]}
            d = inc(d)

        sup13e0 = [{"val":person.fio}]+sup2
        for i in range(12):
            supp[i]+=sup[i]

        dif = [person.fio]+diffx(person)

        dif13.append(dif)
        sup13e.append(sup13e0)

    delta = ['Дельта']+[0]*12
    for i in range(12):
        delta[i+1] = round(supp[i]-dem[i],2)

    moon12["del13"] = delta

    zo = zero('Аутсорс')
    zv = zero('Вакансии')
    sup13 = ['Поставка']+supp

    dem13.append(sup13)
    dem13.append(zo)
    dem13.append(zv)
    dem13.append(delta)
    moon12["dem130"]=dem13
    moon12["dem12"]=dem
    moon12["sup13e"]=sup13e
    moon12["dif13"] = dif13


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    return render(request,'ajr.html',moon12)


def aj(request,j):
    moon12 = moon();
    dem14 = []
    dem13L = []
    sup = []
    dem13R=[]
    dif14 = []

    project = Project.objects.get(id=j)
    roles = Role.objects.all()
    # supp = [0]*12
    # sup139 = []
    sup14 = []
    dif13 = []
    dem1 = []
    sup13=[]
    sup100=[]



    zo = zero('Аутсорс')
    zv = zero('Вакансии')

    for role in roles:

        pz = [role.title]
        dem = [role.title]+['Потребность']+demand(project,role)#----------------
        dem1 = demand(project,role)#--------
        delta = ['Дельта']+[0]*12

        dem2=[0]*12
        d = date.today().replace(day=15)
        for i in range(12):

            x={"link":f"{role.id}.{d.year}-{d.month}-15","title":dem1[i]}
            dem2[i]=x
            d = inc(d)

        dem13R.append([role.title]+dem2)#--------



        p9 = role.title
        people = UserProfile.objects.filter(role=role)
        px = role.title#######################
        supp = [-1,'Поставка']+[0]*12
        p100 = role.title
        for person in people:

            dif = [person.fio]+diffx(person)
            dif14.append([px]+dif)######################
            px = -1##################################

            sup = supply(project,person)
            sup100=[p100,person.fio]+sup
            p100=-1
            for i in range(12):
                supp[i+2]+=sup[i]
            sup14.append(sup100)


        dem13L.append(dem)##########################################
        dem13L.append(supp)###############--
        dem13L.append([-1]+zo)################
        dem13L.append([-1]+zv)#####################

        for i in range(12):
            delta[i+1] = round(supp[i+2]-dem[i+2],2)

        dem13L.append([-1]+delta)############################

    moon12["dem13R"]=dem13R#####################
    moon12["dem13L"]=dem13L###############################
    moon12["sup14"]=sup14


    moon12["dif14"] = dif14########################################
    moon12["role"] = role
    moon12["project_id"] = j
    moon12["project"] = project
    return render(request,'aj.html',moon12)

def ar(request,r):
    moon12 = moon();
    dem14 = []
    dem13L = []
    sup = []
    dem13R=[]
    dif14 = []

    projects = Project.objects.all()
    role = Role.objects.get(id=r)
    people = UserProfile.objects.filter(role=role)
    # supp = [0]*12
    # sup139 = []
    sup14 = []
    dif13 = []
    dem1 = []
    sup13=[]
    sup100=[]



    zo = zero('Аутсорс')
    zv = zero('Вакансии')


    for project in projects:

        pz = [project.title]
        dem = [project.title]+['Потребность']+demand(project,role)#----------------
        dem1 = [project.title]+demand(project,role)#----------------------------

        dem2=[{"val":project.title}]+[0]*12

        d = date.today().replace(day=15)
        for i in range(12):
            dem2[i+1]={"link":f"{project.id}.{d.year}-{d.month}-15","val":dem1[i+1]}
            d = inc(d)

        dem13R.append(dem2)#--------


        #-----------------------------------------
        delta = ['Дельта']+[0]*12
        p9 = project.title
        supp = [-1,'Поставка']+[0]*12
        p100 = project.title
        supp100=[p100]
        for person in people:
            sup = supply(project,person)
            sup=[p100,person.fio]+sup

            # p100=-1
            # for i in range(12):
            #     supp100[i+1]+=sup[i]
            # supp100=[person.fio]+supp100

        dem13L.append(dem)##########################################
        dem13L.append(supp)###############--
        dem13L.append([-1]+zo)################
        dem13L.append([-1]+zv)#####################

        for i in range(12):
            delta[i+1] = round(supp[i+2]-dem[i+2],2)


        sup14.append(sup)
        dem13L.append([-1]+delta)############################
    px = role.title#######################
    for person in people:
        dif = diffx(person)
        dif100=[]
        da = date.today().replace(day=15)
        for i in range(12):
            dif100.append({"link":f"{person.id}.{da.year}-{da.month}-15","title":dif[i]})
            da = inc(da)
        dif14.append([px]+[person.fio]+dif100)######################
        px = -1##################################

    moon12["dem13R"]=dem13R#####################
    moon12["dem13L"]=dem13L###############################
    moon12["sup14"]=sup14


    moon12["dif14"] = dif14########################################
    moon12["role"] = role
    moon12["r"]=role.id
    moon12["project"] = project
    return render(request,'ar.html',moon12)




def dr(request,r):
    moon12 = moon();
    dem14 = []
    dem13L = []
    sup = []
    dem13R=[]
    dif14 = []

    projects = Project.objects.all()
    role = Role.objects.get(id=r)
    people = UserProfile.objects.filter(role=role)
    # supp = [0]*12
    # sup139 = []
    sup14 = []
    dif13 = []
    dem1 = []
    sup13=[]
    sup100=[]



    zo = zero('Аутсорс')
    zv = zero('Вакансии')


    for project in projects:

        pz = [project.title]
        dem = [project.title]+['Потребность']+demand(project,role)#----------------
        dem1 = [project.title]+demand(project,role)#----------------------------

        dem2=[{"val":project.title}]+[0]*12

        d = date.today().replace(day=15)
        for i in range(12):
            dem2[i+1]={"link":f"{project.id}.{d.year}-{d.month}-15","val":dem1[i+1]}
            d = inc(d)

        dem13R.append(dem2)#--------


        #-----------------------------------------
        delta = [project.title]+[0]*12
        p9 = project.title
        supp = [-1,'Поставка']+[0]*12
        p100 = project.title
        supp100=[p100]
        for person in people:
            sup = supply(project,person)
            sup=[p100,person.fio]+sup

            # p100=-1
            # for i in range(12):
            #     supp100[i+1]+=sup[i]
            # supp100=[person.fio]+supp100

        # dem13L.append(dem)##########################################
        # dem13L.append(supp)###############--
        # dem13L.append([-1]+zo)################
        # dem13L.append([-1]+zv)#####################

        for i in range(12):
            delta[i+1] = round(supp[i+2]-dem[i+2],2)


        sup14.append(sup)
        dem13L.append(delta)############################!!!!!!!!!!!!!!!
    px = role.title#######################
    for person in people:
        dif = diffx(person)
        dif100=[]
        da = date.today().replace(day=15)
        for i in range(12):
            dif100.append({"link":f"{person.id}.{da.year}-{da.month}-15","title":dif[i]})
            da = inc(da)
        dif14.append([px]+[person.fio]+dif100)######################
        px = -1##################################

    moon12["dem13R"]=dem13R#####################
    moon12["dem13L"]=dem13L###############################
    moon12["sup14"]=sup14


    moon12["dif14"] = dif14########################################
    moon12["role"] = role
    moon12["r"]=role.id
    moon12["project"] = project
    return render(request,'dr.html',moon12)



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
    return date(y,m,15)

################################################

def inc_n(d,n):
    for i in range(n):
        d = inc(d)
    return d

from datetime import datetime
def tr(person, role, m, l):##########################################
    print(701)
    try:
        instance = Less.objects.get(person=person, start_date=m)
    except:
        instance = None
        print(702)
    if instance:
        print(703)
        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one
        print(704)
        instance = Less.objects.create(person=person, start_date=m, load=l)
        print(705)

def tjr(p, j, d, l):
    print(1578)
    try:

        instance = Task.objects.get(person=p,project=j, month=d)
    except:
        instance = None

    if instance:

        instance.load = l
        instance.save()
    else:

        instance = Task.objects.create(person=p, project=j, month=d, load=l)


def tj(project,role, d, v):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@s
    print(1515)
    m = datetime.strptime(d, "%Y-%m-%d").date()
    print(1998)
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None
    print(299)
    if instance:
        instance.load = float(v)
        instance.save()

        print(499)
    else:
        x = float(v)
        instance = Load.objects.create(project=project, role=role, month=m, load=x)
        print(699)

def dif(d1,d2):
    return (d2.year-d1.year)*12+d2.month-d1.month+1

def pref(p):
    L = []
    L.append(p.general.fio)

    L.append({"title":p.title,"link":p.id})

    L.append(p.start_date)
    L.append(p.end_date)
    return L

def sr(request):
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sr = request.POST.get('r')
            r = int(sr)
            role=Role.objects.get(id=r)

            for k,v in request.POST.items():
                print(k,v)
                if '.' in k:
                    p,d=k.split('.')
                    print(161)
                    try:
                        person = UserProfile.objects.get(id=p)
                        print(1615)
                        tr(person,role,d,v)
                    except:
                        pass
        else:
            print(form.errors)

    return ar(request,r)
def sjr(request):
    print(778)
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k,v in request.POST.items():
                sr = request.POST.get('r')
                r = int(sr)
                role=Role.objects.get(id=r)

                sj = request.POST.get('id')
                j = int(sj)
                project = Project.objects.get(id=j)

                print(k,v)
                if '.' in k:
                    p,d=k.split('.')

                    try:
                        print(678)
                        person = UserProfile.objects.get(id=p)
                        print(679)
                        tjr(person,project,d,v)
                        print(680)
                    except:
                        pass
        else:
            print(form.errors)

        return ajr(request,j,r)
def sj(request):
    print(779)
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k,v in request.POST.items():
                sid = request.POST.get('id')
                j = int(sid)
                project = Project.objects.get(id=j)
                print(k,v)
                if '.' in k:
                    r,d=k.split('.')
                    role = Role.objects.get(id=r)
                    try:
                        print(67878)
                        tj(project,role,d,v)
                        print(67879)
                    except:
                        pass
        else:
            print(form.errors)

        return aj(request,j)
