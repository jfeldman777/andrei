from django.views import View
import numpy as np
from .export import time_difference
from django.db.models import Max

def time_n(d):
    return time_difference(d,date0())

class BalanceNum(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []

        self.flag = True

        self.nProject = Project.objects.all().aggregate(Max('id'))['id__max']
        self.nRole = Role.objects.all().aggregate(Max('id'))['id__max']
        self.nPerson = UserProfile.objects.all().aggregate(Max('id'))['id__max']

        self.IdsProject = list(Project.objects.all().values_list('id', flat=True))
        self.IdsRole = list(Role.objects.all().values_list('id', flat=True))
        self.IdsPerson = list(UserProfile.objects.all().values_list('id', flat=True))

        self.nTime = 12

        user_role_list = list(UserProfile.objects.all().values('id', 'role'))
        self.user_role_dict = {item['id']: item['role'] for item in user_role_list}

        prj_start_list = list(Project.objects.all().values('id', 'start_date'))
        self.prj_start_dict = {item['id']: item['start_date'] for item in prj_start_list}

        prj_end_list = list(Project.objects.all().values('id', 'end_date'))
        self.prj_end_dict = {item['id']: item['end_date'] for item in prj_end_list}

        return

    def setAVLprt(self):
        avls = Less.objects.all()
        for a in avls:
            self.AVL[a.person,self.get_role_id(a.role),time_n(a.start_date)-1]=a.load
        for p in IdsPerson:
            for r in IdsRole:
                for t in range(nTime):
                    if self.AVL[p,r,t]==0:
                        if t == 0 and self.user_role_dict[p]==r:
                            self.AVL[p,r,t]==100
                        else:
                            self.AVL[p, r, t] == self.AVL[p,r,t-1]
        return

    def setNEEDSrjt(self):
        needs = Load.objects.all()
        for a in needs:
            self.NEEDS[a.role,a.project,time_n(a.month)-1]=a.load

        return

    def setWORK(self):
        works = Task.objects.all()
        for a in works:
            self.WORK[a.person,a.role,time_n(a.month)-1]=a.load

    def set_R_W_rest(self):
        for p in IdsPerson:
            for r in IdsRole:
                for t in range(nTime):
                    for j in IdsProject:
                        self.R_W_rest[p,r,t] -= self.WORK[p,r,j,t]
        return

    def set_N_W_balance(self):
        for p in IdsPerson:
            for r in IdsRole:
                for t in range(nTime):
                    for j in IdsProject:
                        self.N_W_balance[p, r, t] -= self.WORK[p, r, j, t]

    def set_PRJtime(self):
        for j in IdsProject:
            d1 = self.prj_start_dict[j]
            d2 = self.prj_end_dict[j]
            for t in range(nTime):
                self.PRJTime = (time_n(d1) <= t) and (time_n(d2) >= t)

        return

    def get_role_id(self,role_id):
        if nRole == 1:
            return 0
        else:
            return role_id

    def get_prj_id(self,prj_id):
        if nProject == 1:
            return 0
        else:
            return prj_id

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

        self.setAVLprt()
        self.NEEDS()
        self.WORK()

        self.R_W_rest = self.AVL.copy()
        self.N_W_balance = self.NEEDS.copy()
        self.PRJtime = np.zeros((nProject,nTime),dtype=bool)

        self.set_R_W_rest()
        self.set_N_W_balance()
        self.set_PRJtime()

        return