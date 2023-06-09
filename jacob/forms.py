from .models import UserProfile
from .models import Project
from django import forms
from django.forms import formset_factory
from .models import Role, Project, UserProfile, Grade, Wish
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл данных для импорта")


class LoadForm(forms.Form):
    role = forms.IntegerField(widget=forms.HiddenInput())
    project = forms.IntegerField(widget=forms.HiddenInput())
    month = forms.CharField(widget=forms.HiddenInput())
    load = forms.FloatField(initial=0)
    label = forms.CharField(widget=forms.TextInput(
        attrs={"readonly": "readonly"}))


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


class User2Form(forms.ModelForm):
    res = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        label="Дополнительный ресурсный пул",
    )

    class Meta:
        model = UserProfile
        fields = ["id", "fio", "role", "res"]
        labels = {
            "role": "Ресурсный пул",
            "fio": "Сотрудник",
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'Пароль': forms.PasswordInput(),
        }
        labels = {
            "username": "Логин",
            "fio": "Сотрудник"
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'fio', 'res', 'virtual']
        labels = {
            "username": "Логин",
            "fio": "Сотрудник"
        }


class UserAndProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Пароль'
    )
    labels = {
        "username": "Логин",
    }
    fio = forms.CharField(label="Сотрудник (ФИО)")
    role = forms.ModelChoiceField(queryset=Role.objects.all(), blank=True, required=False,
                                  label="Ресурсный пул"
                                  )  # Assuming Role model is defined

    res = forms.ModelMultipleChoiceField(queryset=Role.objects.all(),
                                         required=False,
                                         label="Дополнительный ресурсный пул")

    class Meta:
        model = User
        fields = ['username', 'password']  # , 'email']
        labels = {
            "username": "Логин",
            # 'email':"Электронная почта"
        }

    def __init__(self, *args, **kwargs):
        super(UserAndProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = User.objects.make_random_password()


class GeneralModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.userprofile.fio


class RoleForm(forms.ModelForm):

    title = forms.CharField(
        label="Название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = GeneralModelChoiceField(label="Руководитель",
                                      queryset=User.objects.filter(userprofile__virtual=False).order_by('userprofile__fio'))

    class Meta:
        model = Role
        fields = ["id", "title", "general",]
        labels = {
            "general": "Руководитель",
            "title": "Роль"
        }


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(label="Начало",
                                 widget=forms.DateInput(attrs={'type': 'date'})
                                 )
    end_date = forms.DateField(label="Окончание",
                               widget=forms.DateInput(attrs={'type': 'date'}, format='%d.%m.%Y'))

    title = forms.CharField(
        label="Название", max_length=30, widget=forms.TextInput(attrs={"size": "30"})
    )

    general = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(virtual=False),
        label="Руководитель",
        empty_label=None,
    )

    class Meta:
        model = Project
        fields = ["id", "title", "general", "start_date", "end_date"]
        labels = {
            "general": "Руководитель",
        }


class ImmutableModelChoiceField(forms.ModelChoiceField):
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['disabled'] = 'disabled'  # Disables the field
        return attrs

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = self.queryset.get(pk=value)
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            return None
        return value


class GradeForm(forms.ModelForm):
    person = ImmutableModelChoiceField(queryset=UserProfile.objects.all(), required=False,
                                       label='Сотрудник')
    role = ImmutableModelChoiceField(queryset=Role.objects.all(), required=False,
                                     label='Роль')

    class Meta:
        model = Grade
        fields = ['person', 'role', 'mygrade']
        labels = {
            "mygrade": "Грейд",
            "role": "Роль",
            "person": "Cотрудник"
        }
