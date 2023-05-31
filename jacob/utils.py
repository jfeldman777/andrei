from .models import Less
from .forms import EntryForm, ProjectForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .vvv import *

def up(a, b):
    if b < 0:
        return f"надо:{a}"
    return f"надо:{a}/есть:{b}"

    
def eva(request, fun):
    return eval(f"{fun}(request)")


def eva2(request, fun):
    return eval(f"{fun}(request,2,2,2)")

def date0():
    d = date.today().replace(day=15)
    return d


def date12():
    d = date.today().replace(day=15)
    d = inc_n(d, 12)
    return d


