from django.shortcuts import render,redirect
from .models import Project, UserProfile, Load, Role, Task
import datetime,math

from django.forms import Form
def index(request):
    return render(request, 'index.html')

def people(request):
    people = UserProfile.objects.all()
    return render(request, 'people.html', {'people': people})

# def tasks(request):
#     form = None
#     return render(request, 'tasks.html',{form:form})



from django.shortcuts import render,redirect,reverse
from django.forms import formset_factory, Form
from .models import Load, Role, Project, UserProfile, Task
from .forms import LoadForm, CellForm

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