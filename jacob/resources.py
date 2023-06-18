# resources.py

from import_export import resources, fields

from .models import UserProfile,Project

class PersonResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class ProjectResource(resources.ModelResource):
    title = fields.Field(attribute='title', column_name='Название')
    general_name = fields.Field(attribute='general__fio', column_name='Руководитель проекта')
    start_date = fields.Field(attribute='start_date', column_name='Начало')
    end_date = fields.Field(attribute='end_date', column_name='Окончание')

    class Meta:
        model = Project
        fields = ('title', 'start_date', 'end_date', 'general_name')
        export_order = ('title', 'general_name', 'start_date', 'end_date')

    def dehydrate_title(self, project):
        return project.title  # 'Название'

    def dehydrate_general_name(self, project):
        return project.general.fio  # 'Руководитель проекта'

    def dehydrate_start_date(self, project):
        return project.start_date  # 'Начало'

    def dehydrate_end_date(self, project):
        return project.end_date  # 'Окончание'
