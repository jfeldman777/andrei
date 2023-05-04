from .forms import EntryForm
from django.shortcuts import render
from .models import Role,Project,Load,UserProfile,Task,Less

def frames40(request):#Балансировка всех проектов и всех ресурсов
    return render(request, 'frames40.html')

import datetime
def correct(data,l,n):
    d1 = datetime.date.today()
    dn = data[n]
    for i in range(12):
        if inside(d1,l.start_date,l.end_date):
            dn[i+3]=l.load
        d1 = inc(d1)
    return data

def mon_bar():
    dat = []
    d = datetime.date.today().replace(day=15)
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

    return render(request, 't/ost.html', {'ost': people,"t12":t12,"data":data,"project":project,
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




         dif = round(num[i]-sum[i],2)
         dat5[i + 1] = f"{dif}"
     data.append(dat1)
     data.append(dat2)
     data.append(dat3)
     data.append(dat4)
     data.append(dat5)



     context = {'data': data,
              "data0":data0,"role":role,
                'project':project,  "experts":experts}
     return render(request, 't/res.html', context)
def index(request):
    return frames40(request)

def page_balances(request):#Входной лист
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
                pass
                # return frames40(request)
            if p == None:
                pass
                # return right(request,r.id)
            if r == None:
                # return left(request,p.id)
                pass
            return render(request, 't/frames42.html',
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


     dat2 = ['']+[0]*12
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
               "data0":data0,"project_id":id,"r":r,"role":role,
                'project':project, }
     return render(request, 't/res01.html', context)


def res10(request, id,r):

     project = Project.objects.get(id=id)

 ##################################
     data0 =mon_bar()
     data=[]

     role = Role.objects.get(id=r)



     dat2 = ['']+[0]*12
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
                "data0":data0,"role":role,
                'project':project}
     return render(request, 't/res10.html', context)



def correctOst(data,l,n):
    d1 = datetime.date.today()
    dn = data[n]
    for i in range(12):
        if inside(d1,l.month,l.month):
            dn[i+3]-=l.load
        d1 = inc(d1)
    return data

def ostatok(request):
    people = UserProfile.objects.all()
    t12 = ['Фамилия','Имя']+mon_bar()
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

    return render(request, 't/ost.html', {'ost': people,"t12":t12,"data":data,"role":role,})

def inside(d,d1,d2):
    b = (d1.year,d1.month) <= (d.year,d.month) <= (d2.year,d2.month)

def frames42(request, pid, rid, project):  # балансировка проекта (обного) и ресурса (одного)
        return render(request, 't/frames42.html', {"pid": pid, "rid": rid, "project": project})