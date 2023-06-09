from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    title = models.CharField(max_length=30)
    general = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="he", default=1
    )

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE,blank=True,null=True)
    fio = models.CharField(max_length=30, default="?")
    res = models.ManyToManyField(Role, related_name="they" ,blank=True,null=True)
    virtual = models.BooleanField(default=False)

    def __str__(self):
        return self.fio


class Project(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    people = models.ManyToManyField(UserProfile, related_name="they")
    general = models.ForeignKey(
        to=UserProfile, on_delete=models.CASCADE, related_name="he", default=1
    )

    def __str__(self):
        return self.title


class Load(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    month = models.DateField()
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    load = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project}:{self.month}({self.role})={self.load} "


class Less(models.Model):
    person = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    load = models.IntegerField(default=0)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.person.fio}({self.role.title})({self.start_date})={self.load} "


class Task(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    month = models.DateField()
    person = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    load = models.IntegerField(default=0)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.project}:{self.month}:{self.person})={self.load} "

class Wish(models.Model):
    mywish = models.CharField(max_length=80, default="?")
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.project}:{self.role}=>{self.mywish}"

class Grade(models.Model):
    GRADE_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]

    person = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    mygrade = models.CharField(max_length=2, choices=GRADE_CHOICES,default='0')

