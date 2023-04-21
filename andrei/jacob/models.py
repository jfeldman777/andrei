from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Load(models.Model):
    project = models.ForeignKey(to=Project, on_delete = models.CASCADE)
    month = models.DateField()
    role = models.ForeignKey(to=Role, on_delete = models.CASCADE)
    load = models.FloatField(default = 0)

    def __str__(self):
        return(f"{self.project}:{self.month}({self.role})={self.load} ")


class Task(models.Model):
    project = models.ForeignKey(to=Project, on_delete = models.CASCADE)
    month = models.DateField()
    person = models.ForeignKey(to=User, on_delete = models.CASCADE)
    load = models.FloatField(default = 0)

    def __str__(self):
        return(f"{self.project}:{self.month}({self.person})={self.load} ")

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #bio = models.TextField(blank=True)
    #birth_date = models.DateField(null=True, blank=True)
    #profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    role = models.ForeignKey(to=Role,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
