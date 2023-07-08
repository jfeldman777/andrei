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

        self.OUTSRC = UserProfile.objects.get(fio='АУТСОРС')
        self.VACANCY = UserProfile.objects.get(fio='ВАКАНСИЯ')

        self.nProject = Project.objects.all().aggregate(Max('id'))['id__max']
        self.nRole = Role.objects.all().aggregate(Max('id'))['id__max']
        self.nPerson = UserProfile.objects.all().aggregate(Max('id'))['id__max']

        self.people = UserProfile.objects.exclude(is_virtual=True).order_by('fio')
        self.IdsPerson = list(self.people.values_list('id', flat=True))

        self.nTime = 12
        return

    def setAVLprt(self):
        if coord == 1:
            avls = Less.objects.filter(role=self.id)
        else:
            avls = Less.objects.filter(project=self.id)
        for a in avls:
            self.AVLprt[a.person,self.get_role_id(a.role)][time_n(a.start_date)-1]=a.load
        for p in IdsPerson:
            for r in IdsRole:
                for t in range(nTime):
                    if self.AVLprt[p,r][t]==0:
                        if t == 0 and self.user_role_dict[p]==r:
                            self.AVLprt[p,r,t]==100
                        else:
                            self.AVLprt[p, r][t] == self.AVLprt[p,r][t-1]
        return

    def setNEEDSrjt(self):
        if coord == 1:
            needs = Load.objects.filter(role=self.id)
        else:
            needs = Load.objects.filter(project=self.id)

        for a in needs:
            self.NEEDSrjt[a.role,a.project][time_n(a.month)-1]=a.load

        return

    def setWORKprjt(self):
        if coord == 1:
            works = Task.objects.filter(role=self.id)
        else:
            works = Task.objects.filter(project=self.id)
        for a in works:
            self.WORKprjt[a.person,a.role,a.project][time_n(a.month)-1]=a.load

    def set_R_W_prt(self):
        self.R_W_prt = self.AVLprt.copy()
        for p in IdsPerson:
            for r in IdsRole:
                for t in range(nTime):
                    for j in IdsProject:
                        self.R_W_prt[p,r][t] -= self.WORKprjt[p,r,j][t]
        return

    def set_N_W_rjt(self):
        self.N_W_rjt = self.NEEDSrjt.copy()
            for r in self.IdsRole:
                for t in range(nTime):
                    for j in self.IdsProject:
                        for p in self.IdsPerdon
                            self.N_W_rjt[r,j][ t] -= self.WORKprjt[p, r, j][ t]

    def set_PRJtime(self):
        for project in selfProjects:
            d1 = project.start_date
            d2 = project.end_date
            for t in range(nTime):
                self.PRJTime = (time_n(d1) <= t) and (time_n(d2) >= t)

        return

    # def get_role_id(self,role_id):
    #     if nRole == 1:
    #         return 0
    #     else:
    #         return role_id
    #
    # def get_prj_id(self,prj_id):
    #     if nProject == 1:
    #         return 0
    #     else:
    #         return prj_id

    def init(self,id,coord=0, mod=0,n=12):
        self.n = n
        self.mod = mod
        self.coord = coord
        self.id = id

        if coord == 0:
            self.nProject = 1
            self.IdsProject = [self.id]
            self.projects = [Project.objects.get(id = self.id)]

            self.roles = Role.objects.all().order_by('title')
            self.IdsRole = list(self.roles.values_list('id', flat=True))



        else:
            self.nRole = 1
            self.IdsRole = [self.id]
            self.roles = [Role.objects.get(id=self.id)]

            self.projects = Project.objects.all().order_by('title')
            self.IdsProject = list(self.projects.values_list('id', flat=True))


        self.AVL = np.zeros((nPerson,nRole),dtype=np.array((nTime),dtype=int))
        self.NEEDS = np.zeros((nRole,nProject),dtype=np.array((nTime),dtype=int))
        self.WORK = np.zeros((nPerson,nRole,nProject),dtype=np.array((nTime),dtype=int))

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

    def get1(self):


        pass
    def get2(self):
        if self.coord == 0:
            for role in IdsRole:
                self.w2.append([role]+self.NEEDSrjt[role,self.id])
        else:
            for project in self.IdsProject:
                self.w2.append([project]+self.NEEDSrjt[self.id,project])

        pass
    def get3(self):

        pass
    def get4(self):

        pass
