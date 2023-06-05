from django import forms
from django.forms import formset_factory
from .models import Role, Project,UserProfile
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User


class LoadForm(forms.Form):
    role = forms.IntegerField(widget=forms.HiddenInput())
    project = forms.IntegerField(widget=forms.HiddenInput())
    month = forms.CharField(widget=forms.HiddenInput())
    load = forms.FloatField(initial=0)
    label = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))


class KeysForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(KeysForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = User.objects.make_random_password()

class EntryForm(forms.Form):
    projects = forms.ModelChoiceField(
        label="Проекты",
        required=True,
        queryset=Project.objects.all(),
        empty_label="выбрать проект",
    )
    roles = forms.ModelChoiceField(
        label="Ресурсы",
        required=True,
        queryset=Role.objects.all(),
        empty_label="выбрать ресурс",
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


from django import forms
from .models import Project

class User2Form(forms.ModelForm):
    res = forms.ModelChoiceField(
        label="дополнительные роли",
        required=False,
        queryset=Role.objects.all(),
        empty_label="выбрать роль",
    )
    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "fio", "res"]
        labels = {
              "role":"основная роль",

            "fio":"ФИО",
            "user":"логин"
            
        }

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'fio', 'res', 'virtual']

class UserAndProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Password'
    )


    role = forms.ModelChoiceField(queryset=Role.objects.all(),
                                  label="основная роль"
    )  # Assuming Role model is defined
    fio = forms.CharField(label="ФИО")
    res = forms.ModelMultipleChoiceField(queryset=Role.objects.all(),
                                         label="дополнительные роли")


    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
            super(UserAndProfileForm, self).__init__(*args, **kwargs)
            self.fields['password'].initial = User.objects.make_random_password()
class RoleForm(forms.ModelForm):

    title = forms.CharField(
        label="название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = forms.ModelChoiceField(
        queryset = User.objects.filter(userprofile__virtual=False),
        label= "руководитель ресурсного пула"
    )
    class Meta:
        model = Role
        fields = ["id", "title", "general",]
        labels = {
            "general": "руководитель",
            "title":"роль"
        }



class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(label="начало", widget=forms.SelectDateWidget)
    end_date = forms.DateField(label="окончание", widget=forms.SelectDateWidget)
    title = forms.CharField(
        label="название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(virtual=False),
        label="руководитель",
        empty_label=None
    )
    class Meta:
        model = Project
        fields = ["id", "title", "general", "start_date", "end_date"]
        labels = {
            "general": "руководитель",
        }
