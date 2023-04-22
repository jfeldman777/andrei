from django import forms
from django.forms import formset_factory
from .models import Role

class LoadForm(forms.Form):
   role = forms.IntegerField(widget=forms.HiddenInput())
   project = forms.IntegerField(widget=forms.HiddenInput())
   month = forms.CharField(widget=forms.HiddenInput())
   load = forms.FloatField()
   label = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))