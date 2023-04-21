from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Role, Project, Load, Task

admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Load)
admin.site.register(Task)

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','role')

admin.site.register(UserProfile, UserProfileAdmin)
