from datetime import datetime
from .views3 import inc

from django.shortcuts import render
from .models import Load, Role, Project, UserProfile, Less



def index(request):
    return render(request, 'index.html')

def t12ym():
   L = []
   d1 = datetime.now()
   for i in range(12):
       L.append({"year":d1.year,"month":d1.month})
       d1 = inc(d1)
       print(d1)
   return L

def inside(d,d1,d2):
    print(d,d1,d2)
    b = (d1.year,d1.month) <= (d.year,d.month) <= (d2.year,d2.month)
    print(b)
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
    n = 0
    for p in people:
        less = Less.objects.all().filter(person = p)
        print(less)
        for l in less:
            data = correct(data,l,n)
        n+=1

    return render(request, 'people.html', {'people': people,"t12":t12,"data":data})



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