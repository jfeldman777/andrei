from datetime import date

from .models import Load, Task, Less
from .utils import inc


def create_or_update_res_max(person:object, role:object, m:date, l:int)->None:  # Доступность
    try:
        instance = Less.objects.get(person=person, role=role, start_date=m)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Less.objects.create(person=person, role=role, start_date=m, load=l)


def create_or_update_task(p:object, r:object, j:object, d:date, l:int)->None:  # Загрузка tjTask
    try:
        instance = Task.objects.get(person=p, project=j, role=r, month=d)
    except:
        instance = None
    if instance:
        instance.load = l
        instance.save()
    else:
        instance = Task.objects.create(person=p, role=r, project=j, month=d, load=l)


from datetime import datetime
def create_or_update_needs(person:object, role:object, project:object, dm:str, svn:str)->None:  # Потребность tjLoad
    print(999,svn,dm)

    if '-' in svn:
        sv,sn = svn.split('-')
        v = int(sv)
        n = int(sn)
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