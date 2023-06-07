from django.shortcuts import redirect, get_object_or_404, render


from .forms import UserAndProfileForm, RoleForm, User2Form, KeysForm, ProjectForm, GradeForm
from .models import UserProfile, Role, Project, Grade


def create_user_and_profile(request):
    button = "Создать"
    instance = None
    if request.method == "POST":
        form = UserAndProfileForm(request.POST, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if form.cleaned_data['role']:
                user_profile = UserProfile.objects.create(user=user,
                                                      role=form.cleaned_data['role'],
                                                      fio=form.cleaned_data['fio'],
                                                     )
            else:
                user_profile = UserProfile.objects.create(user=user,
                                                          fio=form.cleaned_data['fio'],
                                                          )

            selected_roles = form.cleaned_data.get('res', [])
            user_profile.res.set(selected_roles)

            return redirect("people")
    else:
        form = UserAndProfileForm()

    return render(request, 'form.html', {'form': form,"button":button})


'''
форма для 
'''
def grade_form(request, pid,rid):
    form = None
    button = "Сохранить"
    person = UserProfile.objects.get(id = pid)
    role = Role.objects.get(id = rid)
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade=form.cleaned_data['mygrade']
            Grade.objects.update_or_crteate(person=pid,role=rid,mygrade=grade)
            return redirect("people")
        else:
            print(form.errors)

    initial_data = {'person': person,'role':role}
    form = GradeForm(initial=initial_data)
    return render(request, "form.html", {"form": form,"title":"Грейд","button":button})

def role_form(request, id=None):
    button = "Создать"
    instance = None
    if id:
        button = "Сохранить"
        instance = get_object_or_404(Role, id=id)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("people")

    else:
        form = RoleForm(instance=instance)
    return render(request, "form.html", {"form": form,"title":"Роль","button":button})

def keys_form(request, id=None):
    button = "Создать"
    instance = None
    if id:
        button = "Сохранить"
    if request.method == "POST":
        form = KeysForm(request.POST, instance=instance)
        if form.is_valid():
            user_profile = form.save(commit=False)
            selected_roles = form.cleaned_data.get('res', None)

            if selected_roles is not None:
                if not isinstance(selected_roles, list):
                    selected_roles = [selected_roles]

                user_profile.res.set(selected_roles)

            return redirect("people")
    else:
        form = KeysForm()
    return render(request, "form.html",  {"form": form, "title": "Сотрудник","button":button})

'''
форма для изменение или создания проекта (если номер не указан)
'''

def project_form(request, id=None):
    button = "Создать"
    instance = None
    if id:
        button = "Сохранить"
        instance = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("prjlist")
    else:
        initial_data = {}
        if instance is not None:
            initial_data = {'general': instance.general.fio}
        form = ProjectForm(instance=instance, initial=initial_data)

    return render(request, "form.html", {"form": form,"title":"Проект","button":button})


'''
форма для изменения человека 
'''
def person_form(request, id):
    button = "Создать"
    instance = None
    if id:
        button = "Сохранить"
        instance = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":
        form = User2Form(request.POST, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['role']:
                user.role_id = form.cleaned_data['role'].id  # Set the foreign key using an ID
            user.save()
            user.res.set(form.cleaned_data['res'])  # Set the many-to-many relationship
            user.save()
            return redirect("people")
    else:
        form = User2Form(instance=instance)
    return render(request, "form.html",  {"form": form,"title":"Сотрудник","button":button})