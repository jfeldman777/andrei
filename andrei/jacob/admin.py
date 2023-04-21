from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Role, Project, Load, Task

admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Load)
admin.site.register(Task)