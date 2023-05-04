from datetime import datetime
from .views3 import inc,projects
from .models import Role


from django.shortcuts import render
from .models import Load, Role, Project, UserProfile, Less, Task
def myotd(request,id):
    mss=t12ym()

    t12 = ['Фамилия','-'] + mss
    data = []
    dat1 = []
    dat2=[]
    num = [1] * 12
    sum = [0] * 12
    sum2 = [0] * 12

    d1 = datetime.now().date()
    role = Role.objects.get(id=id)
    experts = UserProfile.objects.filter(role=id).order_by('id')
    mss = t12ym()
    for person in experts:
        user = UserProfile.objects.get(id=person.id).user
        dat1 = [{"title":user.last_name,"link":person.id},'доступно']
        dat2 = [{"title": user.last_name, "link": person.id},'занято']
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

        dat1 += [sum[i] for i in range(12)]
        dat2 += [sum2[i] for i in range(12)]

        data.append(dat1)
        data.append(dat2)
    context = {'data': data, 't12': t12,'role_id':id,'role':role,}


    return render(request, 'myotd.html',context)
# def homeleft(request):
#     return render(request, 'homeleft.html')
#
# def homeright(request):
#     return render(request, 'homeright.html')

def details(request):
    return render(request, 'details.html')

def myprj(request,pid):
    return render(request, 'left.html')
def myprj2(request):
    return render(request, 'left.html')
def otdlist(request):
    roles = Role.objects.all().order_by('id')
    people = UserProfile.objects.all().order_by('role')
    mss=t12ym()

    t12 = ['Роль','='] + mss
    data = []
    d1 = datetime.now().date()
    d2 = inc_n(d1,12)
    for r in roles:
        dat = []
        dat2 = []
        num = [1] * 12
        sum = [0] * 12
        sum2 = [0] * 12
        dat.append({'title':r,'link':r.id})
        dat2.append({'title': r, 'link': r.id})
        dat.append('доступно')
        dat2.append('занято')
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

        dat+=[sum[i] for i in range(12)]
        dat2 += [sum2[i] for i in range(12)]
        data.append(dat)
        data.append(dat2)
    context = {'data': data, 't12': t12,}
    return render(request,'otdlist.html',context)

def prjlist(request):
    return projects(request)

#
# def index(request):
#     return render(request, 'frames42.html')



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
            if inside(d, l.start_date, l.end_date):
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