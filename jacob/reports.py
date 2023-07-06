from datetime import date, datetime

from django.shortcuts import render

from .db import time_available_in_date, time_available, real_and_virtual_people, get_prj_triplet, real_people
from .models import UserProfile, Task, Project
from .paint import Paint


def my_date(m):
    d = datetime.strptime(m, "%Y-%m-%d").date().replace(day=15)
    return d

def get_workload_prm(p,r,d):
    ts = Task.objects.filter(person=p, role=r, month=d)
    res = 0
    for t in ts:
        res += t.load
    #res = sum(ts.load)
    return res

def get_workload_prjm(p,r,j,d):
    ts = Task.objects.filter(person=p, role=r, project=j, month=d)
    res = 0
    for t in ts:
        res += t.load
    #res = sum(ts.load)
    return res
def get_workload_prjm(p,r,j,m):
    person,role,project = get_prj_triplet(p,r,j)
    res = 0
    d = my_date(m)
    t = Task.objects.filter(person=person, project=project, role=role, month=d)
    try:
        res = t[0].load
    except:
            pass
    return res

#time_available(person,role,d)



def report_by_prm(request,r,y,m):
    w = []
    d = date(y,m,15)
    people = real_people(r)
    for p in people:
        avl = time_available(p, r, d)
        twl = get_workload_prm(p, r, d)
        line = {"fio":p.fio,"avl":avl,"twl":twl,"delta":(avl-twl),
                "color":my_color(avl-twl)}
        w.append(line )

    return render(request,"report_prm.html",{"w":w})
def report_by_prjm(request,r,y,m):
    w = []
    d = date(y,m,15)
    people = real_people(r)
    projects = Project.objects.all()
    for j in projects:
        for p in people:
            avl = time_available(p, r, d)
            twl = get_workload_prjm(p, r, j, d)
            line = {"prj":j,"fio":p.fio,"avl":avl,"twl":twl,"delta":(avl-twl),
                    "color":my_color(avl-twl)}
            w.append(line )

    return render(request,"report_prjm.html",{"w":w})

def my_color(val):
    if val < -100 :
        return Paint.MY_BLUE
    if val > 0 :
        return Paint.MY_PINK
    if val < 0 :
        return Paint.MY_GREEN
    return ""