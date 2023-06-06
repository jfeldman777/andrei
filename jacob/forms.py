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

class UsernameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.username

class User2Form(forms.ModelForm):
    res = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        label="Дополнительные роли",
    )

    class Meta:
        model = UserProfile
        fields = ["id", "fio", "role", "res"]
        labels = {
            "role": "Основная роль",
            "fio": "ФИО",
         }


#
# class User2Form(forms.ModelForm):
#     user = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly': 'readonly'}),
#         label='Логин',
#     )
#     res = forms.ModelMultipleChoiceField(queryset=Role.objects.all(),   required=False,
#                                          label="Дополнительные роли")
#     class Meta:
#         model = UserProfile
#         fields = ["id", "user", "role", "fio", "res"]
#         labels = {
#               "role":"Основная роль",
#
#             "fio":"ФИО",
#             "user":"Логин"
#
#         }
#     def __init__(self, *args, **kwargs):
#             super(User2Form, self).__init__(*args, **kwargs)
#             if self.instance and self.instance.pk:
#                 self.fields['user'].initial = self.instance.user.username

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'Пароль': forms.PasswordInput(),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'fio', 'res', 'virtual']

class UserAndProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Пароль'
    )


    role = forms.ModelChoiceField(queryset=Role.objects.all(),
                                  label="Основная роль"
    )  # Assuming Role model is defined
    fio = forms.CharField(label="ФИО")
    res = forms.ModelMultipleChoiceField(queryset=Role.objects.all(),
                                         label="Дополнительные роли")


    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
            super(UserAndProfileForm, self).__init__(*args, **kwargs)
            self.fields['password'].initial = User.objects.make_random_password()
class RoleForm(forms.ModelForm):

    title = forms.CharField(
        label="Название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = forms.ModelChoiceField(
        queryset = User.objects.filter(userprofile__virtual=False),
        label= "Руководитель ресурсного пула"
    )
    class Meta:
        model = Role
        fields = ["id", "title", "general",]
        labels = {
            "general": "Руководитель",
            "title":"Роль"
        }



class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(label="Начало", widget=forms.SelectDateWidget)
    end_date = forms.DateField(label="Окончание", widget=forms.SelectDateWidget)
    title = forms.CharField(
        label="Название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(virtual=False),
        label="Руководитель",
        empty_label=None
    )
    class Meta:
        model = Project
        fields = ["id", "title", "general", "start_date", "end_date"]
        labels = {
            "general": "Руководитель",
        }
