from .models import Less
from .forms import EntryForm, ProjectForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

def people_of_rv(role):
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


def people_of_rr(role):
    pp1 = set(UserProfile.objects.filter(Q(role=role, virtual=False)))
    pp2 = set(UserProfile.objects.filter(Q(res=role, virtual=False)))
    pps = pp1.union(pp2)
    ppl = sorted(list(pps), key=lambda x: x.fio)
    return ppl


def is_virt(person):
    if person.fio in ("ВАКАНСИЯ", "АУТСОРС"):
        return True
    return False


def vacancia(role, project):
    try:
        person = UserProfile.objects.filter(fio="ВАКАНСИЯ")[0]  ##АУТСОРС
    except:
        person = None
    return prj_task_(person, role, project)


def outsrc(role, project):
    try:
        person = UserProfile.objects.filter(fio="АУТСОРС")[0]
    except:
        person = None
    return prj_task_(person, role, project)
