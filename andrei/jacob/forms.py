from django import forms
from django.forms import formset_factory
from .models import Role,Project

class LoadForm(forms.Form):
   role = forms.IntegerField(widget=forms.HiddenInput())
   project = forms.IntegerField(widget=forms.HiddenInput())
   month = forms.CharField(widget=forms.HiddenInput())
   load = forms.FloatField(initial=0)
   label = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

class CellForm(LoadForm):
   person = forms.IntegerField(widget=forms.HiddenInput())

# forms.py
from django import forms

class UpdateFloatForm(forms.Form):
    person_id = forms.IntegerField(widget=forms.HiddenInput())
    project_id = forms.IntegerField(widget=forms.HiddenInput())
    year = forms.IntegerField(widget=forms.HiddenInput())
    month = forms.IntegerField(widget=forms.HiddenInput())
    load = forms.FloatField(label='занятость в проекте')

from django import forms
from django.forms import formset_factory

class TableCellForm(forms.Form):
    cell_value = forms.FloatField()

def table_to_formset(table):
    formset = formset_factory(TableCellForm, extra=0)
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            data.append({'cell_value': cell.text})
    return formset(initial=data)

from django import forms

class EntryForm(forms.Form):
    projects = forms.ModelChoiceField(label='Проекты',required=False,
                    queryset=Project.objects.all(), empty_label='выбрать проект',)
    roles = forms.ModelChoiceField(label='Ресурсы',required=False,
        queryset=Role.objects.all(), empty_label='выбрать ресурс', )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


from django import forms

class MyForm(forms.Form):
    CHOICES = [('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3')]
    my_field = forms.MultipleChoiceField(choices=CHOICES, widget=forms.SelectMultiple(attrs={'size':10}))
