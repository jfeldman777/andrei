from django.db import models

# Create your models here.
from django.db import models

class Role(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
