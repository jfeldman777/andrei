from datetime import datetime
from .views3 import inc,projects
from .models import Role
# from .views3 import inc_n

from django.shortcuts import render
from .models import Load, Role, Project, UserProfile, Less, Task
def homeleft(request):
    return render(request, 'homeleft.html')

def homeright(request):
    return render(request, 'homeright.html')

def myotd(request,id):
    mss=t12ym()

    t12 = ['Фамилия'] + mss
    data = []
    dat = []
    num = [1] * 12
    sum = [0] * 12
    sum2 = [0] * 12

    d1 = datetime.now().date()
    role = Role.objects.get(id=id)
    experts = UserProfile.objects.filter(role=id).order_by('id')
    mss = t12ym()
    for person in experts:
        user = UserProfile.objects.get(id=person.id).user
        dat = [user.last_name]
        num = [1] * 12
        sum = [0] * 12
        sum2 = [0] * 12
        less = Less.objects.filter(person=person).order_by('id')
        for l in less:
            print(l)
            d = d1
            for i in range(12):
                if inside(d, l.start_date, l.end_date):
                    num[i] = l.load
                    print(l.load, i)
                d = inc(d)
        for i in range(12):
            sum[i] += num[i]
        i = 0
        for m in mss:
            d = datetime(year=m['year'], month=m['month'], day=15)
            tasks = Task.objects.filter(person=person, month=d)

            for task in tasks:
                t = task.load
                sum2[i] += t
            i += 1
            num = [1] * 12

        dat+=[{'plus':sum[i],'minus':sum2[i]} for i in range(12)]
        data.append(dat)
    context = {'data': data, 't12': t12,'role_id':id,'role':role,}


    return render(request, 'myotd.html',context)
def homeleft(request):
    return render(request, 'homeleft.html')

def homeright(request):
    return render(request, 'homeright.html')

def myprj2(request):
    return render(request, 'left.html')
def otdlist(request):
    roles = Role.objects.all().order_by('id')
    people = UserProfile.objects.all().order_by('role')
    mss=t12ym()

    t12 = ['Роль'] + mss
    data = []
    d1 = datetime.now().date()
    d2 = inc_n(d1,12)
    for r in roles:
        dat = []
        num = [1] * 12
        sum = [0] * 12
        sum2 = [0] * 12
        dat.append({'title':r,'link':r.id})
        n = 0
        print(r)
        experts = UserProfile.objects.filter(role=r)
        for person in experts:
            less = Less.objects.filter(person = person).order_by('id')
            for l in less:
                print(l)
                d = d1
                for i in range(12):
                    if inside(d,l.start_date,l.end_date):
                        num[i]=l.load
                        print(l.load, i)
                    d = inc(d)
            for i in range(12):
                sum[i]+=num[i]
            i=0
            for m in mss:
                d = datetime(year=m['year'],month=m['month'],day=15)
                tasks = Task.objects.filter(person=person,month=d)

                for task in tasks:
                    t = task.load
                    sum2[i]+=t
                i+=1
            num = [1] * 12

        dat+=[{'plus':sum[i],'minus':sum2[i]} for i in range(12)]

        data.append(dat)
    context = {'data': data, 't12': t12,}
    return render(request,'otdlist.html',context)

def prjlist(request):
    return projects(request)


def index(request):
    return render(request, 'frames42.html')



def t12ym():
   L = []
   d1 = datetime.now()
   for i in range(12):
       L.append({"year":d1.year,"month":d1.month})
       d1 = inc(d1)

   return L

def inside(d,d1,d2):
    b = (d1.year,d1.month) <= (d.year,d.month) <= (d2.year,d2.month)

    return b

def correct(data,l,n):
    d1 = datetime.now().date()
    dn = data[n]
    for i in range(12):
        if inside(d1,l.start_date,l.end_date):
            dn[i+3]=l.load
        d1 = inc(d1)
    return data

def people(request):
    people = UserProfile.objects.all().order_by("role")
    t12 = ['Роль','Фамилия','Имя']+t12ym()
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
        print(k, i,data[k][i+3] )
        k+=1
    return render(request, 'people.html', {'people': people,"t12":t12,"data":data})

def inc_n(d,n):
    for i in range(n):
        d = inc(d)
    return d

def tasks(person,d):
    res = 0
    tasks = Task.objects.all().filter(person=person,month = d)
    for t in tasks:
        res += t.load
    return res

def dost(person,ms):
    d1 = datetime.date(ms)
    less = Less.objects.all().filter(person=person).order_by("id")
    for l in less:
        if inside(d1, l.start_date, l.end_date):
            res = l.load
    pass


def ost(person,ms):
    return dost(person,ms)-tasks(person,ms)


def correctOst(data,l,n):
    d1 = datetime.now().date()
    dn = data[n]
    for i in range(12):
        if inside(d1,l.month,l.month):
            dn[i+3]-=l.load
        d1 = inc(d1)
    return data

def ostatok(request):
    people = UserProfile.objects.all().order_by("role")
    t12 = ['Роль','Фамилия','Имя']+t12ym()
    data = [([p.role,p.user.last_name,p.user.first_name]+[1]*12) for p in people]
    n = 0
    for p in people:


        less = Less.objects.all().filter(person = p)
        for l in less:
            data = correct(data,l,n)

        tasks = Task.objects.all().filter(person=p)
        for t in tasks:
            data = correctOst(data,t,n)
        n+=1

    return render(request, 'ost.html', {'ost': people,"t12":t12,"data":data})

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