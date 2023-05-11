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

            return ajr(request,p.id,r.id)

    form = EntryForm()
    return render(request,'alf.html', {'form': form})
def atj(request):
    projects = Project.objects.all().order_by ('general')
    data = []
    for p in projects:
        x = {"j":p.id,
            "project":p.title,
        "name":p.general.fio}
        data.append(x)
    context = {"data":data}

    return render(request,'atj.html',context)

def atr(request):
    context = {}
    roles = Role.objects.all().order_by ('general')
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {
            "title":p.title,"r":p.id,
        "name":u.fio}
        data2.append(x)
    context["data2"]=data2

    return render(request,'atr.html',context)
def att(request):
    projects = Project.objects.all().order_by ('general')
    data = []
    for p in projects:
        x = {"j":p.id,
            "project":p.title,
        "name":p.general.fio}
        data.append(x)
    context = {"data":data}

    roles = Role.objects.all().order_by ('general')
    data2 = []
    for p in roles:
        u = UserProfile.objects.get(user=p.general)
        x = {
            "title":p.title,"r":p.id,
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
def supply2(project,person):
        sp=[0]*12
        d = date.today().replace(day=15)
        for i in range(12):
            L = list(Task.objects.filter(project=project,month=d,person=person))
            try:
                t = L[0].load
            except:
                t = 0

            sp[i]={"link":f"{project.id}.{person.id}.{d.year}-{d.month}-15","val":t}
            d = inc(d)
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

def demand2(project,role):
    dem = [0]*12
    d = date.today().replace(day=15)
    for i in range(12):
        L = list(Load.objects.filter(project=project,month=d,role=role))
        try:
            t = L[0].load
        except:
            t = 0

        dem[i]={"link":f"{d.year}-{d.month}-15","val":t}
        d = inc(d)
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
def djr(request,j,r):
    moon12 = moon();
    dem13 = []
    sup13e = []
    sup13 = []
    dif13 = []

    project = Project.objects.get(id=j)
    role = Role.objects.get(id=r)
    dem2 = demand2(project,role)
    dem = demand(project,role)
    # dem13.append(['Потребность']+dem)

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

    delta = [0]*12
    for i in range(12):
        delta[i] = round(supp[i]-dem[i],2)


    dem13.append(delta)
    moon12["dem130"]=dem13
    moon12["dem12"]=dem2
    moon12["sup13e"]=sup13e
    moon12["dif13"] = dif13


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    return render(request,'djr.html',moon12)

def ajr(request,j,r):
    moon12 = moon();
    dem13 = []
    sup13e = []
    sup13 = []
    dif13 = []

    project = Project.objects.get(id=j)
    role = Role.objects.get(id=r)
    dem = demand(project,role)
    dem2 = demand2(project,role)
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
    moon12["dem12"]=dem2
    moon12["sup13e"]=sup13e
    moon12["dif13"] = dif13


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    return render(request,'ajr.html',moon12)


def dj(request,j):
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
        delta = [0]*12

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

        for i in range(12):
            delta[i] = round(supp[i+2]-dem[i+2],2)

        dem13L.append([role.title]+delta)############################

    moon12["dem13R"]=dem13R#####################
    moon12["dem13L"]=dem13L###############################
    moon12["sup14"]=sup14


    moon12["dif14"] = dif14########################################
    moon12["role"] = role
    moon12["project_id"] = j
    moon12["project"] = project
    moon12["j"] = j
    return render(request,'dj.html',moon12)



def  mro(request):
    moon12 = moon();
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()



    for role in roles:
        p9 = role.title
        people = UserProfile.objects.filter(role=role)
        px = role.title#######################
        for person in people:

            dif = [person.fio]+diffx(person)
            dif14.append([px]+dif)######################
            px = -1##################################

    moon12["dif14"] = dif14########################################

    return render(request,'mro.html',moon12)

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
    moon12["j"] = j
    return render(request,'aj.html',moon12)
def mj(request,j):
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
    moon12["j"] = j
    return render(request,'mj.html',moon12)

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
    sup13e=[]
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
        supp100=[p100]+[0]*12
        for person in people:
            sup = supply(project,person)
            sup2 = [0]*12

            d = date.today().replace(day=15)
            for i in range(12):
                sup2[i]={"link":f"{project.id}.{person.id}.{d.year}-{d.month}-15","val":sup[i]}
                d = inc(d)

            sup13e0 = [p100,{"val":person.fio}]+sup2
            p100=-1
            sup13e.append(sup13e0)
            for i in range(12):
                supp[i+2]+=sup[i]

            # sup=[p100,person.fio]+sup#######################################s




            # for i in range(12):
            #      supp[i+2]+=sup[i+2]

        dem13L.append(dem)##########################################77777
        dem13L.append(supp)###############--
        dem13L.append([-1]+zo)################
        dem13L.append([-1]+zv)#####################

        for i in range(12):
            delta[i+1] = round(supp[i+2]-dem[i+2],2)



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
    moon12["sup13e"]=sup13e


    moon12["dif14"] = dif14########################################
    moon12["role"] = role
    moon12["r"]=r
    moon12["project"] = project

    return render(request,'ar.html',moon12)

def mr(request,r):
    moon12 = moon();
    dif14 = []

    role = Role.objects.get(id=r)
    people = UserProfile.objects.filter(role=role)

    for person in people:
        dif = less(person)

        dif100=[0]*12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i]={"link":f"{person.id}.{da.year}-{da.month}-15","title":dif[i]}
            da = inc(da)
        dif14.append([person.fio]+dif100)######################

    moon12["dif14"] = dif14########################################
    moon12["r"]=r
    moon12["role"]=role

    return render(request,'mr.html',moon12)



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
            sup = supply2(project,person)
            sup=[p100]+[{"val":person.fio}]+sup

            sup14.append(sup)

            p100=-1
            # for i in range(12):88888

            sup = supply(project,person)
            sup=[p100,person.fio]+sup############################################s
            sup14.append(sup)


            p100=-1
            for i in range(12):
                 supp[i+2]+=sup[i+2]



        for i in range(12):
            delta[i+1] = round(supp[i+2]-dem[i+2],2)



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

    try:
        instance = Less.objects.get(person=person, start_date=m)
    except:
        instance = None

    if instance:

        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one

        instance = Less.objects.create(person=person, start_date=m, load=l)
def tdr(project,person,  m, l):##########################################

    try:
        instance = Task.objects.get(person=person, project=project,month=m)
    except:
        instance = None

    if instance:

        instance.load = l
        instance.save()
    else:
        # If the instance does not exist, create a new one

        instance = Task.objects.create(person=person, project=project,month=m, load=l)


def tjr(p, j, d, l):

    try:

        instance = Task.objects.get(person=p,project=j, month=d)
    except:
        instance = None

    if instance:

        instance.load = l
        instance.save()
    else:

        instance = Task.objects.create(person=p, project=j, month=d, load=l)


def tj(project,role, m, v):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@s
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None

    if instance:
        instance.load = float(v)
        instance.save()

    else:
        instance = Load.objects.create(project=project, role=role, month=m, load=v)

def dif(d1,d2):
    return (d2.year-d1.year)*12+d2.month-d1.month+1

def pref(p):
    L = []
    L.append(p.general.fio)

    L.append({"title":p.title,"link":p.id})

    L.append(p.start_date)
    L.append(p.end_date)
    return L

def smr(request):
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

                if '.' in k:
                    p,d=k.split('.')

                    try:
                        person = UserProfile.objects.get(id=p)

                        tr(person,role,d,v)
                    except:
                        pass
        else:
            print(form.errors)

    return mr(request,r)

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
                if '.' in k:
                    j,p,d=k.split('.')

                    try:
                        person = UserProfile.objects.get(id=p)
                        project = Project.objects.get(id=j)

                        tdr(project,person,d,v)
                    except:
                        pass
        else:
            print(form.errors)

    return ar(request,r)


def sdr(request):
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
                    j,p,d=k.split('.')

                    try:

                        person = UserProfile.objects.get(id=p)
                        project = Project.objects.get(id=j)
                        tdr(project,person,d,v)

                    except:
                        pass
        else:
            print(form.errors)
    return ar(request,r)

def sdrd(request):
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
                    j,p,d=k.split('.')

                    try:

                        person = UserProfile.objects.get(id=p)
                        project = Project.objects.get(id=j)
                        tdr(project,person,d,v)

                    except:
                        pass
        else:
            print(form.errors)

    return dr(request,r)


def sdjr(request):
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sr = request.POST.get('r')
            r = int(sr)
            role = Role.objects.get(id=r)
            sj = request.POST.get('id')
            j = int(sj)
            project = Project.objects.get(id=j)

            for k,v in request.POST.items():

                if '-' in k:
                    try:
                        tj(project,role,k,v)
                    except:
                        pass
        else:
            print(form.errors)

    return djr(request,j,r)

def sjr(request):

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

                if '.' in k:
                    p,d=k.split('.')

                    try:

                        person = UserProfile.objects.get(id=p)

                        tj(person,project,d,v)##################################

                    except:
                        pass
        else:
            print(form.errors)

        return ajr(request,j,r)

def sjrL(request):

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

                if '.' in k:
                    p,d=k.split('.')

                    try:

                        person = UserProfile.objects.get(id=p)

                        tjr(person,project,d,v)

                    except:
                        pass
        else:
            print(form.errors)

        return djr(request,j,r)

def sjrR(request):

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

                if '-' in k:

                    try:
                        tj(project,role,k,v)
                    except:
                        pass
        else:
            print(form.errors)

        return ajr(request,j,r)
def sj(request):

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k,v in request.POST.items():
                sid = request.POST.get('id')
                j = int(sid)
                project = Project.objects.get(id=j)

                if '.' in k:
                    r,d=k.split('.')
                    role = Role.objects.get(id=r)
                    try:

                        tj(project,role,d,v)

                    except:
                        pass
        else:
            print(form.errors)

        return aj(request,j)
def smj(request):

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for k,v in request.POST.items():
                sid = request.POST.get('id')
                j = int(sid)
                project = Project.objects.get(id=j)

                if '.' in k:
                    r,d=k.split('.')
                    role = Role.objects.get(id=r)
                    try:

                        tj(project,role,d,v)

                    except:
                        pass
        else:
            print(form.errors)

        return mj(request,j)
def projects(request):
    dmin = date.today()
    dmin=dmin.replace(day=15)
    dmax = inc_n(dmin,11)
    moon12 = moon();
    projects = Project.objects.all().order_by('general','start_date')

    data = []
    for p in projects:
        data.append(pref(p)+[dif(p.start_date,p.end_date)]+mon_bool(dmin,dmax,p.start_date,p.end_date))

    moon12["matrix"]=data

    return render(request, 'prjlist.html', moon12)

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
