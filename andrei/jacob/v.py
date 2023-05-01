from django.shortcuts import render
from .forms import EntryForm
from .models import Project,Role


def entry(request):#Входной лист
    p = None
    r = None
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
                return frames40(request)
            if p == None:
                return right(request,r.id)
            if r == None:
                return left(request,p.id)
            return frames42(request,p.id,r.id,project)
    else:
        form = EntryForm()
    return render(request, 'entry.html', {'form': form,"project":project})
def frames42(request,pid,rid,project):#балансировка проекта (обного) и ресурса (одного)
    return render(request, 'frames42.html',{"pid":pid,"rid":rid,"project":project})
def frames40(request):#Балансировка всех проектов и всех ресурсов
    return render(request, 'frames40.html')
def left(request,pid):#конкретный проект
    return render(request, 'leftframe.html',{'id':pid})

def right(request,rid):#конкретный ресурс
    return render(request, 'rightframe.html',{'id':rid})