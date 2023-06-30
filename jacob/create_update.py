from datetime import date

from .db import time_available_in_date, time_available
from .log import log
from .models import Load, Task, Less, Wish, Role, Project
from .utils import inc, timespan_len, inc_n


def create_or_update_wish(role:Role, project:Project, txt:str)->None:  # Доступность
    try:
        instance = Wish.objects.get(role=role, project=project)
    except:
        instance = None
    if instance:
        instance.mywish = txt
        instance.save()
    else:
        instance = Wish.objects.create(project=project, role=role, mywish=txt)



def create_or_update_res_max(person:object, role:object, m:date, svn:str)->None:  # Доступность

    d = datetime.strptime(m, "%Y-%m-%d").date()
    if '-' in svn:
        sv,sn = svn.split('-')
        v = int(sv)
        try:
            n = int(sn)
        except:
            n = -1
    else:
        v = int(svn)
        n = 1

    if n < 0:
        Less.objects.filter(person=person, role=role, start_date__gte=d).delete()
        Less.objects.create(person=person, role=role, start_date=d, load=v)

    else:
        d1 = inc_n(d,n)
        v1 = time_available(person,role,d)
        print(v,v1,d,d1,role,person)
        log(f"v={v}  \n")
        log(f"v1={v1}    \n")
        log(f"d={d}     \n")
        log(f"d1={d1}")
        log(f"person={person} \n")
        log(f"role={role}      \n")

        Less.objects.filter(person=person, role=role, start_date__range=(d, d1)).delete()

        Less.objects.create(person=person, role=role, start_date=d, load=v)
        Less.objects.create(person=person, role=role, start_date=d1, load=v1 )




def create_or_update_task(p:object, r:object, j:object, dm:date, svn:str)->None:  # Загрузка
    d2 = j.end_date
    d = datetime.strptime(dm, "%Y-%m-%d").date()
    if '-' in svn:
        sv,sn = svn.split('-')
        v = int(sv)
        try:
            n = int(sn)
        except:
            n = timespan_len(d, d2)

    else:
        v = int(svn)
        n = 1

    for i in range(n):
        try:
            instance = Task.objects.get(person=p, project=j, role=r, month=d)
        except:
            instance = None
        if instance:
            try:
                instance.load = v
                instance.save()
            except:
                print("bad1")
        else:
            try:
                instance = Task.objects.create(person=p, role=r, project=j, month=d, load=v)
                print(2022)
            except:
                print("bad")
        d = inc(d)


from datetime import datetime
def create_or_update_needs(person:object, role:object, project:object, dm:str, svn:str)->None:  # Потребность tjLoad
    d2 = project.end_date
    d = datetime.strptime(dm, "%Y-%m-%d").date()
    if '-' in svn:
        sv,sn = svn.split('-')
        v = int(sv)
        try:
            n = int(sn)
        except:
            n = timespan_len(d, d2)
    else:
        v = int(svn)
        n = 1
    m = datetime.strptime(dm, "%Y-%m-%d").date()
    print(m)
    print(n)
    for i in range(n):
        try:
            instance = Load.objects.get(project=project, role=role, month=m)
        except:
            instance = None
            print(project,role,m)

        if instance:
            try:
                instance.load = v
                instance.save()
                print(888,v)
            except:
                print('bad2')

        else:
            try:
                instance = Load.objects.create(project=project, role=role, month=m, load=v)
            except:
                print('bad')

        print(m)
        m = inc(m)
        print(m)