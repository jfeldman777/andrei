from .models import Less
from .forms import EntryForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q


def get_prj(p,r,j):
    role=None
    if r>0:
        role = Role.objects.get(id=r)
    person = None
    if p>0:
        person = UserProfile.objects.get(id=p)
    project = None
    if j>0:
        project = Project.objects.get(id=j)

    return (person,role,project)

def people_of_r(role):
    pp = UserProfile.objects.filter(Q(role = role)|Q(res = role))
    print(pp)
    return pp

def prjm_task(request,p,r,j,y,m):
    d = date(y,m,15)#.replace(year=y).replace(month=m).replace(day=15)
    person,role,project=get_prj(p,r,j)
    task = Task.objects.filter(project=project,person=person,role = role,month=d)
    context = {"t":task}
    return render(request,'a_test.html',context)

def prm_isfree(request,p,r,y,m):
    res = prm_isfree_(p,r,y,m)
    context = {"t":res}
    return render(request,'a_test.html',context)

def prm_isfree_(p,r,y,m):
    d = date(y,m,15)#.replace(year=y).replace(month=m).replace(day=15)
    person,role,project=get_prj(p,r,-1)
    if person.role == role:
        t = 100
    elif role in person.res:
        t = 0
    task = Less.objects.filter(person=person,role = role,start_date__lte = d).order_by('-start_date')
    try:
        t = task[0].load
    except:
        pass
    return t
def rjm_load(request,r,j,y,m):
    d = date(y,m,15)#.replace(year=y).replace(month=m).replace(day=15)
    person,role,project=get_prj(-1,r,j)
    task = Load.objects.filter(project=project,role = role,month=d)
    context = {"t":task}
    return render(request,'a_test.html',context)

def pr_dif(request,p,r):
    t = pr_dif_(p,r)
    context = {"t":t}
    return render(request,'a_test.html',context)

def pr_dif_(p,r):
    c = [0]*12
    a = pr_task_(p,r)
    b = pr_isfree_(p,r)
    for i in range(12):
        c[i] = b[i]-a[i]
    return c

def pr_task(request,p,r):
    res = pr_task_(p,r)
    context = {"t":res}
    return render(request,'a_test.html',context)

def pr_task_(person,role):
    d = date.today().replace(day=15)
    res = [0]*12
    for i in range(12):
        tasks = Task.objects.filter(person=person,role = role,month=d)
        for task in tasks:
            try:
                res[i]+=task.load
            except:
                pass
        d = inc(d)
    return res

def prm_task(request,p,r,y,m):
    d = date(y,m,15)
    t = 0
    person,role,project=get_prj(p,r,-1)

    tasks = Task.objects.filter(person=person,role = role,month=d)
    for task in tasks:
        try:
            t+=task.load
        except:
            pass

    context = {"t":t}
    return render(request,'a_test.html',context)

def prj_task(request,p,r,j):
    person,role,project=get_prj(p,r,j)
    res = prj_task_(person,role,project)
    context = {"t":res}
    return render(request,'a_test.html',context)

def prj_task_(p,r,j):
    d = date.today().replace(day=15)
    res = [0]*12
    for i in range(12):
        t = Task.objects.filter(person=p,project=j,role = r,month=d)
        try:
            res[i]+=t[0].load
        except:
            pass
        d = inc(d)
    return res


def rj_task_(r,j):
    d = date.today().replace(day=15)
    res = [0]*12
    for i in range(12):
        t = Task.objects.filter(project=j,role = r,month=d)
        try:
            res[i]+=t[0].load
        except:
            pass
        d = inc(d)
    return res
def pr_isfree(request,p,r):
    res = pr_isfree_(p,r)
    context = {"t":res}
    return render(request,'a_test.html',context)
def pr_isfree_(person,role):
    res = [0]*12
    d = date.today().replace(day=15)#.replace(year=y).replace(month=m).replace(day=15)
    t = -1
    if person.role == role:
        t = 100
    elif  person.res.filter(id=role.id).exists():
        t = 0

    for i in range(12):
        task = Less.objects.filter(person=person,role = role,start_date__lte = d).order_by('-start_date')
        try:
            t = task[0].load
        except:
            pass
        res[i]=t
        d = inc(d)
    return res

def rj_load(request,r,j):
    person,role,project=get_prj(-1,r,j)
    res = rj_load_(role,project)
    context = {"t":res}
    return render(request,'a_test.html',context)

def rj_load_(r,j):
    d = date.today().replace(day=15)
    res = [0]*12
    for i in range(12):
        t = Load.objects.filter(project=j,role = r,month=d)
        try:
            res[i]=t[0].load
        except:
            pass
        d = inc(d)
    return res

def rj_delta_(r,j):
    a = rj_load_(r,j)
    b = rj_task_(r,j)
    c = [0]*12
    for i in range(12):
        c[i] = b[i] - a[i]
    return c

def date0():
    d = date.today().replace(day=15)
    return d

def date12():
    d = date.today().replace(day=15)
    d = inc_n(d,12)
    return d


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

def diffx(person,role):


    return pr_dif_(person,role)


def moon():
    y_data = []
    m_data = []
    ym = []
    d = date.today().replace(day=15)
    for i in range(12):
            y_data.append(d.year)
            m_data.append(d.month)
            ym.append({"y":d.year,"m":d.month})
            d = inc(d)
    return {"yy":y_data,"mm":m_data,"ym":ym}
    ##################################################################
def djr(request,j,r):
    person,role,project=get_prj(-1,r,j)
    w4=[]
    w3=[]
    w2=[]
    w1=[]
    moon12 = moon()
    delta = rj_delta_(role,project)

    w4=[]


    diff = [0]*12
    people = people_of_r(role)
    for person in people:#7777777777777777777777777777777777777777
        w4.append([person.fio]+pr_dif_(person,role))

    a_w2=[0]*12
    dem_rj = rj_load_(role,project)#----------------


    d = date.today().replace(day=15)
    for i in range(12):
        a_w2[i]=    {"link":f"{d.year}-{d.month}-15","val":dem_rj[i],
            "up":up(max(-delta[i],0),diff[i]),
        }#

        d = inc(d)
    w2=a_w2



    for person in people:
        b_w3 = [0]*12
        a_w3 = prj_task_(person,role,project)

        d = date.today().replace(day=15)
        for i in range(12):
            color = ""
            if delta[i] < 0:
                color="mypink"
            b_w3[i] = {"link":f"{person.id}.{d.year}-{d.month}-15",
            "up":up(
            max(-delta[i],0)
            ,diff[i]),
            "val":a_w3[i],
            "color":color

            }
            d = inc(d)

        c_w3 = [{"val":person.fio}]+b_w3
        p100=-1
        w3.append(c_w3)

    w1.append(delta)############################
    moon12["w1"]=w1
    moon12["w2"]=w2
    moon12["w3"]=w3
    moon12["w4"] = w4


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    return render(request,'djr.html',moon12)

def ajr(request,j,r):
    person,role,project=get_prj(-1,r,j)
    w4=[]
    w3=[]
    w2=[]
    w1=[]
    moon12 = moon()
    supp = [-1,'Поставка']+rj_task_(role,project)
    delta = ['Дельта']+rj_delta_(role,project)
    zo = zero('Аутсорс')
    zv = zero('Вакансии')
    w4=[]


    diff = [0]*12
    people = people_of_r(role)
    for person in people:#7777777777777777777777777777777777777777
        w4.append([person.fio]+pr_dif_(person,role))

    a_w2=[0]*12
    dem_rj = ['Потребность']+rj_load_(role,project)#----------------


    d = date.today().replace(day=15)
    for i in range(12):
        a_w2[i]=    {"link":f"{d.year}-{d.month}-15","val":dem_rj[i+1],
            "up":up(max(-delta[i+1],0),diff[i]),

        }#

        d = inc(d)
    w2=a_w2

    supp = ['Поставка']+rj_task_(role,project)
    delta = ['Дельта']+rj_delta_(role,project)

    for person in people:
        b_w3 = [0]*12
        a_w3 = prj_task_(person,role,project)

        d = date.today().replace(day=15)
        for i in range(12):

            color=""
            if delta[i+1] < 0:
                color="mypink"
            b_w3[i] = {"link":f"{person.id}.{d.year}-{d.month}-15",
            "up":up(
            max(-delta[i+1],0)
            ,diff[i]),
            "val":a_w3[i],
            "color":color

            }



            d = inc(d)

        c_w3 = [{"val":person.fio}]+b_w3
        p100=-1
        w3.append(c_w3)

    w1.append(dem_rj)##########################################77777
    w1.append(supp)###############--
    w1.append(zo)################
    w1.append(zv)#####################
    w1.append(delta)############################
    moon12["w1"]=w1
    moon12["w2"]=w2
    moon12["w3"]=w3
    moon12["w4"] = w4


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    moon12["r"] = r
    moon12["j"] = j
    return render(request,'ajr.html',moon12)


def dj(request,j):
    person,role,project=get_prj(-1,-1,j)
    w4=[]
    w3=[]
    w2=[]
    w1=[]
    moon12 = moon()
    supp = [-1,'Поставка']+rj_task_(role,project)
    delta = ['Дельта']+rj_delta_(role,project)
    zo = zero('Аутсорс')
    zv = zero('Вакансии')
    w4=[]

    people = people_of_r(role)
    for person in people:#7777777777777777777777777777777777777777
        diff=pr_dif_(person,role)
        w4.append([person.fio]+diff)


    a_w2=[0]*12
    dem_rj = rj_load_(role,project)#----------------

        #sdiff=pr_dif_(person,role)
    d = date.today().replace(day=15)
    for i in range(12):

        a_w2[i]=    {"link":f"{d.year}-{d.month}-15","val":dem_rj[i],
            #"up":up(max(-delta[i+1],0),diff[i]),
        }#

        d = inc(d)
    w2=a_w2


    delta = ['Дельта']+rj_delta_(role,project)

    for person in people:
        b_w3 = [0]*12
        a_w3 = prj_task_(person,role,project)
        diff=pr_dif_(person,role)
        d = date.today().replace(day=15)
        for i in range(12):
            b_w3[i] = {"link":f"{person.id}.{d.year}-{d.month}-15",
            "up":up(
            max(-delta[i+1],0)
            ,diff[i]),
            "val":a_w3[i]}
            d = inc(d)

        c_w3 = [{"val":person.fio}]+b_w3
        p100=-1
        w3.append(c_w3)


    w1.append(delta)############################
    moon12["w1"]=w1
    moon12["w2"]=w2
    moon12["w3"]=w3
    moon12["w4"] = w4


    moon12["role"] = role

    moon12["project"] = project
    moon12["id"] = j
    #moon12["r"] = r
    moon12["j"] = j
    return render(request,'dj.html',moon12)


def  mrom(request):
    moon12 = moon();
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()

    my = UserProfile.objects.all()
    arr = [0]*100
    for p in my:
        arr[p.id] = [0]*1000
        for r in roles:
            t = pr_isfree_(p,r)
            arr[p.id][r.id]=[0]*12
            for i in range(12):
                arr[p.id][r.id][i]+=t[i]

    for role in roles:
        p9 = role.title
        people = people_of_r(role)
        px = role.title#######################
        for person in people:
            dif2 = [{"val":person.fio}]+[0]*12
            dif = [person.fio]+pr_isfree_(person,role)
            for i in range(12):

                if arr[person.id][role.id][i] > 100:
                    color = "red"
                else:
                    color = "white"

                dif2[i+1] = {
                "color":color,
                "val":dif[i+1]
                }

            dif14.append([px]+dif2)######################
            px = -1##################################

    moon12["dif14"] = dif14########################################

    return render(request,'mrom.html',moon12)

def  mro(request):
    moon12 = moon();
    dif14 = []

    project = Project.objects.all()
    roles = Role.objects.all()
    for role in roles:
        p9 = role.title
        people = people_of_r(role)
        px = role.title#######################
        for person in people:

            dif = [person.fio]+diffx(person,role)
            dif14.append([px]+dif)######################
            px = -1##################################

    moon12["dif14"] = dif14########################################

    return render(request,'mro.html',moon12)

def aj(request,j):
    moon12 = moon();
    w1=[]
    w2=[]
    w3=[]
    w4=[]
    project = Project.objects.get(id=j)
    roles = Role.objects.all()

    zo = zero('Аутсорс')
    zv = zero('Вакансии')

    for role in roles:
        pz = [role.title]
        dem = [role.title]+['Потребность']+rj_load_(role,project)#----------------
        delta = ['Дельта']+rj_delta_(role,project)

        dem2=[0]*12
        d = date.today().replace(day=15)
        for i in range(12):

            x={"link":f"{role.id}.{d.year}-{d.month}-15",
            "title":dem[i+2]}            
            dem2[i]=x
            d = inc(d)

        w2.append([role.title]+dem2)#--------



        p9 = role.title
        people = people_of_r(role)
        px = role.title
        supp = [-1,'Поставка']+[0]*12
        p100 = role.title
        for person in people:
            dif = [person.fio]+diffx(person,role)
            w4.append([px]+dif)######################
            px = -1##################################

            sup = pr_task_(person,role)
            sup100=[p100,person.fio]+sup
            p100=-1
            for i in range(12):
                supp[i+2]+=sup[i]
            w3.append(sup100)


        w1.append(dem)##########################################
        w1.append(supp)###############--
        w1.append(zo)################
        w1.append(zv)#####################
        
        delta = rj_delta_(role,project)

        w1.append(['Дельта']+delta)############################

    moon12["w2"]=w2#####################
    moon12["w1"]=w1###############################
    moon12["w3"]=w3


    moon12["w4"] = w4  ########################################
    moon12["role"] = role
    moon12["project_id"] = j
    moon12["project"] = project
    moon12["j"] = j
    return render(request,'aj.html',moon12)
def mj(request,j):
    moon12 = moon()
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

            x={"link":f"{role.id}.{d.year}-{d.month}-15",
            "up":up(1,2),
            "title":dem1[i]}#9898
            dem2[i]=x
            d = inc(d)

        dem13R.append([role.title]+dem2)#--------




        people = UserProfile.objects.filter(role=role)
        px = role.title#######################
        supp = [-1,'Поставка']+[0]*12
        p100 = role.title
        for person in people:

            dif = [person.fio]+diffx(person,role)
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
            delta[i+1] = round(supp[i+2]-dem[i+2])

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
    person,role,project=get_prj(-1,r,-1)
    people = people_of_r(r)
    w3=[]
    w2=[]
    w1=[]
    moon12 = moon()
    projects = Project.objects.all()

    zo = zero('Аутсорс')
    zv = zero('Вакансии')
#W222222222222222222222222222222
    for project in projects:
        a_w2=[{"val":project.title}]+[0]*12
        dem_rj = [project.title]+['Потребность']+rj_load_(role,project)#

        d = date.today().replace(day=15)
        for i in range(12):
            a_w2[i+1]={"val":dem_rj[i+2]}#9898
            d = inc(d)
        w2.append(a_w2)#--------


        supp = [-1,'Поставка']+rj_task_(role,project)
        delta = ['Дельта']+rj_delta_(role,project)


        w4=[]


        x=[0]*12
        p100 = project.title
        for person in people:
            x=pr_dif_(person,role)
            w4.append([person.fio]+x)

            b_w3 = [0]*12
            a_w3 = prj_task_(person,role,project)

            d = date.today().replace(day=15)



            for i in range(12):

                color=""
                if delta[i+1] < 0:
                    color="mypink"
                b_w3[i] = {"link":f"{person.id}.{d.year}-{d.month}-15",
                "up":up(
                max(-delta[i+1],0),diff[i]),
                "val":a_w3[i],
                "color":color

                }
##########################################################################3333333
                d = inc(d)

            c_w3 = [p100,{"val":person.fio}]+b_w3
            p100=-1
            w3.append(c_w3)

        w1.append(dem_rj)##########################################77777
        w1.append(supp)###############--
        w1.append([-1]+zo)################
        w1.append([-1]+zv)#####################
        w1.append([-1]+delta)############################

    moon12["w4"] = w4########################################
    moon12["w2"]=w2#####################
    moon12["w1"]=w1###############################
    moon12["w3"]=w3



    moon12["role"] = role
    moon12["r"]=r
    moon12["project"] = project

    return render(request,'ar.html',moon12)
########################################################################
def smr(request):
    id = 1
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
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
def mr(request,r):
    moon12 = moon()
    dif14 = []

    role = Role.objects.get(id=r)
    people = people_of_r(r)

    for person in people:
        dif = less(person)

        dif100=[0]*12
        da = date.today().replace(day=15)
        for i in range(12):
            dif100[i]={"link":f"{person.id}.{da.year}-{da.month}-15",
            "up":up(1,2),
            "title":dif[i]}#9898
            da = inc(da)
        dif14.append([person.fio]+dif100)######################

    moon12["dif14"] = dif14########################################
    moon12["r"]=r
    moon12["role"]=role

    return render(request,'mr.html',moon12)


def dr(request,r):
    person,role,project=get_prj(-1,r,-1)
    people = people_of_r(r)
    w3=[]
    w2=[]
    w1=[]
    moon12 = moon()
    projects = Project.objects.all()

#W222222222222222222222222222222
    for project in projects:
        a_w2=[{"val":project.title}]+[0]*12
        dem_rj = [project.title]+['Потребность']+rj_load_(role,project)#----------------
        d = date.today().replace(day=15)
        for i in range(12):
            a_w2[i+1]={"val":dem_rj[i+1]}#9898
            d = inc(d)
        w2.append(a_w2)#--------

        delta = rj_delta_(role,project)


        w4=[]


        x=[0]*12
        p100 = project.title
        for person in people:
            x=pr_dif_(person,role)
            w4.append([person.fio]+x)

            b_w3 = [0]*12
            a_w3 = prj_task_(person,role,project)

            d = date.today().replace(day=15)
            for i in range(12):
                b_w3[i] = {"link":f"{project.id}.{person.id}.{d.year}-{d.month}-15",
                "up":up(
                max(-delta[i],0)
                ,x[i]),
                "val":a_w3[i]}
                d = inc(d)

            c_w3 = [p100,{"val":person.fio}]+b_w3
            p100=-1
            w3.append(c_w3)

        w1.append([project.title]+delta)############################

    moon12["w4"] = w4########################################
    moon12["w2"]=w2#####################
    moon12["w1"]=w1###############################
    moon12["w3"]=w3



    moon12["role"] = role
    moon12["r"]=r
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

def tjTask(p,r, j, d, l):
    print(909,p,j,d,l)
    try:
        instance = Task.objects.get(person=p,project=j, role=r,month=d)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Task.objects.create(person=p, role=r, project=j, month=d, load=l)


def tjLoad(project,role, m, v):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@s
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None

    if instance:
        instance.load = float(v)
        instance.save()

    else:
        instance = Load.objects.create(project=project, role=role, month=m, load=v)

def s5(request):
    print(969)
    id = 1
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            sr = request.POST.get('r')
            r = int(sr)
            for k,v in request.POST.items():

                if '.' in k:
                    j,p,d=k.split('.')

                    try:
                        role = Role.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)
                        project = Project.objects.get(id=j)
                        print(456)
                        tjTask(person,role,project,d,v)
                        print(457)

                    except:
                        pass
        else:
            print(form.errors)
    return ar(request,r)

def s6(request):
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
                        role = Rle.objects.get(id=r)
                        person = UserProfile.objects.get(id=p)
                        project = Project.objects.get(id=j)
                        tjTask(person,role,project,d,v)
                    except:
                        pass
        else:
            print(form.errors)

    return dr(request,r)


def s4(request):
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
                        tjLoad(project,role,k,v)
                    except:
                        pass
        else:
            print(form.errors)
    return djr(request,j,r)

def s1(request):
    if request.method == "POST":
        form = Form(request.POST)
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
                        tjTask(person,role,project,d,v)##################################
                    except:
                        pass
        else:
            print(form.errors)

    return ajr(request,j,r)

def s3(request):
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

                        tjTask(person,role,project,d,v)

                    except:
                        pass
        else:
            print(form.errors)

    return djr(request,j,r)

def s2(request):
    if request.method == "POST":
        form = Form(request.POST)
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
                        tjLoad(project,role,k,v)
                    except:
                        pass
        else:
            print(form.errors)
    return ajr(request,j,r)
def sj(request):
    j=1
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

                        tjLoad(project,role,d,v)

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

                        tjLoad(project,role,d,v)

                    except:
                        pass
        else:
            print(form.errors)

        return mj(request,j)
def projects(request):
    dmin = date.today()
    dmin=dmin.replace(day=15)
    dmax = inc_n(dmin,11)
    moon12 = moon()
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
def pref(p):
    L = []
    L.append(p.general.fio)

    L.append({"title":p.title,"link":p.id})#989898

    L.append(p.start_date)
    L.append(p.end_date)
    return L
def up(a,b):
    return f"надо:{a}/есть:{b}"