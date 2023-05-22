from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Role, Project, Load, Task, Less

admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Load)
admin.site.register(Task)
admin.site.register(Less)

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','fio','role')
    # ordering=['user.last_name']

admin.site.register(UserProfile, UserProfileAdmin)