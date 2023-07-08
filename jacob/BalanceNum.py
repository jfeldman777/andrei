from django.shortcuts import render
from django.views import View
import numpy as np
from .utils import timespan_len,date0
from .models import UserProfile,Project,Role,Less,Load,Task
from django.db.models import Max

def time_n(d):
    return timespan_len(d,date0())

class BalanceNum(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []

        self.OUTSRC = UserProfile.objects.get(fio='АУТСОРС')
        self.VACANCY = UserProfile.objects.get(fio='ВАКАНСИЯ')

        self.nProject = Project.objects.all().aggregate(Max('id'))['id__max']+1
        self.nRole = Role.objects.all().aggregate(Max('id'))['id__max']+1
        self.nPerson = UserProfile.objects.all().aggregate(Max('id'))['id__max']+1

        self.people = UserProfile.objects.exclude(virtual=True).order_by('fio')
        self.IdsPerson = list(self.people.values_list('id', flat=True))

        people_list = list(self.people.values('id', 'role'))
        self.people_dict = {item['id']: item['role'] for item in people_list}

        self.nTime = 12
        return
    def get_role_id(self,role_id):
        if self.nRole == 1:
            return 0
        else:
            return role_id

    def get_prj_id(self,prj_id):
        if self.nProject == 1:
            return 0
        else:
            return prj_id

    def get(self,request,id,coord,mod):
        self.init(id,coord,mod)
        self.get2()
        return render(request,'nb.html',{'w':self.w2})

    def setAVLprt(self):
        if self.coord == 1:
            avls = Less.objects.filter(role=self.id)
        else:
            avls = Less.objects.all()
        for a in avls:
            p = a.person
            r = a.role
            t = time_n(a.start_date)   #-1
            self.AVLprt[p.id,r.id,t]=a.load
        try:
            for p in self.IdsPerson:
                for r in self.IdsRole:
                    for t in range(self.nTime):
                        print(p,r,t)
                        if self.AVLprt[p,r,t]==0:
                            if t == 0 and self.people_dict[p]==r:
                                self.AVLprt[p,r,t]==100
                            else:
                                self.AVLprt[p, r,t] == self.AVLprt[p,r,t-1]
        except:
            print(p,r,t)

        return

    def setNEEDSrjt(self):
        if self.coord == 1:
            needs = Load.objects.filter(role=self.id)
        else:
            needs = Load.objects.filter(project=self.id)

        for a in needs:
            try:
                r = a.role
                j = a.project
                t = time_n(a.month)
                print(r,j,t)
                try:
                    self.NEEDSrjt[r,j,t]=a.load
                except:
                    print(r,j,t)
            except:
                print(a)
        return

    def setWORKprjt(self):
        if self.coord == 1:
            works = Task.objects.filter(role=self.id)
        else:
            works = Task.objects.filter(project=self.id)
        for a in works:
            try:
                self.WORKprjt[a.person,a.role,a.project][time_n(a.month)]=a.load
            except:
                print(101)

    def set_R_W_prt(self):
        self.R_W_prt = self.AVLprt.copy()
        for p in self.IdsPerson:
            for r in self.IdsRole:
                for t in range(self.nTime):
                    for j in self.IdsProject:
                        try:
                            self.R_W_prt[p,r,t] -= self.WORKprjt[p,r,j,t]
                        except:
                            pass
        return

    def set_N_W_rjt(self):
            self.N_W_rjt = self.NEEDSrjt.copy()
            for r in self.IdsRole:
                for t in range(self.nTime):
                    for j in self.IdsProject:
                        for p in self.IdsPerson:
                            try:
                                self.N_W_rjt[r,j, t] -= self.WORKprjt[p, r, j, t]
                            except:
                                pass

    def set_PRJtime(self):
        for project in self.projects:
            d1 = project.start_date
            d2 = project.end_date
            for t in range(self.nTime):
                self.PRJTime = (time_n(d1) <= t) and (time_n(d2) >= t)

        return


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


        self.AVLprt = np.zeros((self.nPerson,self.nRole,self.nTime),dtype=int)
        self.NEEDSrjt = np.zeros((self.nRole,self.nProject,self.nTime),dtype=int)
        self.WORKprjt = np.zeros((self.nPerson,self.nRole,self.nProject,self.nTime),dtype=int)

        self.setAVLprt()
        self.setNEEDSrjt()
        self.setWORKprjt()

        self.R_W_prt = self.AVLprt.copy()
        self.N_W_rjt = self.NEEDSrjt.copy()
        self.PRJtime = np.zeros((self.nProject,self.nTime),dtype=bool)

        self.set_R_W_prt()
        self.set_N_W_rjt()
        self.set_PRJtime()

        return

    def get1(self):


        pass
    def get2(self):
        if self.coord == 0:
            for role in self.IdsRole:
                try:
                    sliced_array = self.NEEDSrjt[role, 0, :]
                    wx = [self.roles[role].title] + sliced_array.tolist()
                    self.w2.append(wx)
                except:
                    pass
        else:
            for project in self.IdsProject:
                try:
                    wx = [project]+self.NEEDSrjt[0,project,:].toList()
                    self.w2.append(wx)
                except:
                    pass

        pass
    def get3(self):

        pass
    def get4(self):

        pass
