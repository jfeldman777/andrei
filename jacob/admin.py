from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Role, Project, Load, Task, Less, Grade, Wish



admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Load)
admin.site.register(Task)
admin.site.register(Less)

from .models import UserProfile

class GradeAdmin(admin.ModelAdmin):
    list_display = ("person", "role", "mygrade")
    ordering=['person']
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "fio", "role")
    ordering=['fio']
class WishAdmin(admin.ModelAdmin):
    list_display = ("project", "role", "mywish")
    ordering=['project','role']

admin.site.register(Wish,WishAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Grade,GradeAdmin)