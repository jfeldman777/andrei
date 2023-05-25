from django import forms
from django.forms import formset_factory
from .models import Role,Project

class LoadForm(forms.Form):
   role = forms.IntegerField(widget=forms.HiddenInput())
   project = forms.IntegerField(widget=forms.HiddenInput())
   month = forms.CharField(widget=forms.HiddenInput())
   load = forms.FloatField(initial=0)
   label = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))



class EntryForm(forms.Form):
    projects = forms.ModelChoiceField(label='Проекты',required=True,
                    queryset=Project.objects.all(), empty_label='выбрать проект',)
    roles = forms.ModelChoiceField(label='Ресурсы',required=True,
        queryset=Role.objects.all(), empty_label='выбрать ресурс', )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'general','start_date','end_date']
        # Дополнительные поля формы
