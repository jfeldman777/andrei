# resources.py

from import_export import resources
from .models import UserProfile

class PersonResource(resources.ModelResource):
    class Meta:
        model = UserProfile
