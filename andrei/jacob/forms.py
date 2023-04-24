from django import forms
from django.forms import formset_factory
from .models import Role

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



