from pickle import TUPLE3
from .models import Less
from .forms import EntryForm, ProjectForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .vvv import *
from .utils import *

def real_and_virtual_people(role:object)->List[object]:
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    pps = pp1.union(pp2)
    ppl = sorted(list(pps), key=lambda x: x.fio)
    try:
        ou = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]
        ov = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        ou = None
        ov = None
    return ppl + [ou, ov]


def real_people(role):
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    pps = pp1.union(pp2)
    ppl = sorted(list(pps), key=lambda x: x.fio)
    return ppl


def is_virtual(person):
    if person.fio in ("ВАКАНСИЯ", "АУТСОРС"):
        return True
    return False




def get_prj(p:int, r:int, j:int)->tuple:
    role = None
    if r > 0:
        try:
            role = Role.objects.filter(id=r)[0]
        except:
            pass
    person = None
    if p > 0:
        try:
            person = UserProfile.objects.filter(id=p)[0]
        except:
            pass
    project = None
    if j > 0:
        try:
            project = Project.objects.filter(id=j)[0]
        except:
            pass

    return (person, role, project)


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