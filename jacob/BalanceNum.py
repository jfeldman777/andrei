from django.views import View
import numpy as np
from .export import time_difference


def time_dif(d1,d2):
    pass

class BalanceNum(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []

        self.flag = True

        self.nProject = Project.objects.count()
        self.nRole = Role.objects.count()
        self.nPerson = UserProfile.objects.count()
        self.nTime = 12


        return

    def setAVLprt(self):
        d = date0()
        avls = Less.objects.all()
        for a in avls:
            r = a.role
            j = a.project



        pass

    def setNEEDS(self):
        pass

    def setWORK(self):
        pass


    def init(self,id,coord=0, mod=0,n=12):
        self.n = n
        self.mod = mod
        self.coord = coord
        self.id = id

        if coord == 0:
            self.nProject = 1
        else:
            self.nRole = 1

        self.AVL = np.zeros((nPerson,nRole,nTime),dtype=int)
        self.NEEDS = np.zeros((nRole,nProject,nTime),dtype=int)
        self.WORK = np.zeros((nPerson,nRole,nProject,nTime),dtype=int)

        self.ProjectIDs = np.zeros((nProject),dtype=int)
        self.RoleIDs = np.zeros((nRole),dtype=int)
        self.PersonIDs = np.zeros((nPerson),dtype=int)

        projects = Project.objects.all().order_by('id')
        i = 0
        for project in projects:
            self.ProjectIDs[i] = project.id
            i += 1

        roles = Role.objects.all().order_by('id')
        i = 0
        for role in roles:
            self.RoleIDs[i]=role.id
            i += 1

        peiople = UderProfile.objects.all().order_by('id')
        i = 0
        for person in people:
            self.PersonIDs = person.id
            i += 1









        if mod > 2:
            pass
        elif mod > 1:
            pass
        else:
            pass

        return