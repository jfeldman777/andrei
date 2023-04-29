# from django import forms
# from .models import Car
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit
#
# class CarForm(forms.Form):
#     car = forms.ModelChoiceField(queryset=Car.objects.all(), empty_label=None)
#
#     def __init__(self, *args, **kwargs):
#         super(CarForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.layout = Layout(
#             'car',
#             Submit('submit', 'Submit')
#         )
#         self.helper.form_method = 'post'

from django.shortcuts import render
from .forms import EntryForm
from .models import Project,Role
from .views import index,right,left,frames

def entry(request):
    p = None
    r = None
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            projects = form.cleaned_data['projects']
            roles = form.cleaned_data['roles']
            if projects:
                p = Project.objects.get(title=projects)
            if roles:
                r = Role.objects.get(title=roles)

            if p== None and r == None:
                return index(request)
            if p == None:
                return right(request,r)
            if r == None:
                return left(request,p)
            return frames(request)
    else:
        form = EntryForm()
    return render(request, 'index.html', {'form': form})
