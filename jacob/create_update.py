from datetime import date

from .models import Load, Task, Less


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



def create_or_update_needs(person:object, role:object, project:object, m:date, v:int)->None:  # Потребность tjLoad
    try:
        instance = Load.objects.get(project=project, role=role, month=m)
    except:
        instance = None

    if instance:
        instance.load = float(v)
        instance.save()

    else:
        instance = Load.objects.create(project=project, role=role, month=m, load=v)
