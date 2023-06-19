
from .models import Role, Project, Load, Task, Less, Grade,UserProfile,Wish

# admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import PersonResource,ProjectResource

#
# class PersonAdmin(ImportExportModelAdmin):
#     resource_class = PersonResource
# @admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("user", "fio", "role")
    ordering=['fio']
    resource_class = PersonResource

class ProjectAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date","general")
    ordering=['start_date']
    resource_class = ProjectResource


admin.site.register(Role)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Load)
admin.site.register(Task)
admin.site.register(Less)
admin.site.register(Wish)


class GradeAdmin(admin.ModelAdmin):
    list_display = ("person", "role", "mygrade")
    ordering=['person']



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Grade,GradeAdmin)