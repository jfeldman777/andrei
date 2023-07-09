from django.shortcuts import render
from django.views import View
import numpy as np
from .utils import timespan_len,date0
from .models import UserProfile,Project,Role,Less,Load,Task
from django.db.models import Max
from .timing import timing_decorator

def time_n(d):
    res = timespan_len(date0(),d)
    return res

class BalanceNum(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []

        self.OUTSRC = UserProfile.objects.get(fio='АУТСОРС')
        self.VACANCY = UserProfile.objects.get(fio='ВАКАНСИЯ')

        self.nProject = Project.objects.all().aggregate(Max('id'))['id__max']+1
        # self.IdsProject = [-1]*self.nProject


        self.nRole = Role.objects.all().aggregate(Max('id'))['id__max']+1
        self.IdsRole = [-1]*self.nRole


        self.nPerson = UserProfile.objects.all().aggregate(Max('id'))['id__max']+1
        self.people = UserProfile.objects.exclude(virtual=True).order_by('fio')

        people_list = list(self.people.values('id', 'role'))
        self.people_dict = {item['id']: item['role'] for item in people_list}

        self.people = list(self.people) + [self.OUTSRC,self.VACANCY]

        self.nTime = 12
        return

    #@timing_decorator
    def get(self,request,id,coord,mod):
        self.init(id,coord,mod)
        self.get2()
        self.get3()
        self.get4()
        context = {'w':self.w4}
        # context['nRole']=self.nRole
        # context['nProject']=self.nProject
        # context['nPerson']=self.nPerson

        # context['IdsRole']=self.IdsRole
        # context['IdsProject']=self.IdsProject
        # context['IdsPerson']=self.IdsPerson
        #
        # context['roles']=self.roles
        # context['projects']=self.projects
        # context['people']=self.people
        #
        # context['needs_ar']=self.NEEDSrjt
        context['needs']=self.R_W_prt
        context['avl']=self.AVLprt
        context['avls']=self.avls
        context['work']=self.WORKprjt
        return render(request,'nb.html',context)

    def setAVLprt(self):
        if self.coord == 1:
            avls = Less.objects.filter(role=self.id)
        else:
            avls = Less.objects.all()
        self.avls=avls
        for a in avls:
            p = a.person
            r = a.role
            t = time_n(a.start_date)   #-1
            self.AVLprt[p.id,r.id,t]=a.load
            print(p.id,r.id,t,a.load,999)

        try:
            for p in self.people:
                for r in self.roles:
                    for t in range(self.nTime):
                        if self.AVLprt[p.id,r.id,t]==0:
                            if t == 0 and self.people_dict[p]==r:
                                self.AVLprt[p.id,r.id,t]==100
                            else:
                                self.AVLprt[p.id, r.id,t] == self.AVLprt[p.id,r.id,t-1]
        except:
            print(p,r,t)

        return

    def setNEEDSrjt(self):
        if self.coord == 1:
            needs = Load.objects.filter(role=self.id)
        else:
            needs = Load.objects.filter(project=self.id)

        self.needs = needs
        for a in needs:
            try:
                r = a.role.id
                j = a.project.id
                t = time_n(a.month)
                try:
                    self.NEEDSrjt[r,j,t]=a.load
                    print(r, j,t,a.load)
                except:
                    print(r,j)
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
                self.WORKprjt[a.person.id,a.role.id,a.project.id,time_n(a.month)]=a.load
            except:
                print(101)

    def set_R_W_prt(self):
        self.R_W_prt = self.AVLprt.copy()
        for p in self.people:
            for r in self.roles:
                for t in range(self.nTime):
                    for j in self.projects:
                        try:
                            self.R_W_prt[p.id,r.id,t] -= self.WORKprjt[p.id,r.id,j.id,t]
                        except:
                            pass
        return

    def set_N_W_rjt(self):
            self.N_W_rjt = self.NEEDSrjt.copy()
            for r in self.roles:
                for t in range(self.nTime):
                    for j in self.projects:
                        for p in self.people:
                            try:
                                self.N_W_rjt[r.id,j.id, t] -= self.WORKprjt[p.id, r.id, j.id, t]
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
            # self.IdsProject[id] = id
            self.projects = [Project.objects.get(id = self.id)]
            self.roles = Role.objects.all().order_by('title')
        else:
            self.roles = [Role.objects.get(id=self.id)]
            self.projects = Project.objects.all().order_by('title')

        self.AVLprt = np.zeros((self.nPerson+1,self.nRole+1,self.nTime),dtype=int)
        self.setAVLprt()

        self.WORKprjt = np.zeros((self.nPerson+1,self.nRole+1,self.nProject+1,self.nTime),dtype=int)
        self.setWORKprjt()

        self.NEEDSrjt = np.zeros((self.nRole+1,self.nProject+1,self.nTime),dtype=int)
        self.setNEEDSrjt()

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
            for r in self.roles:
                    try:
                        wx = [r.title] + self.NEEDSrjt[r.id, self.id, :].tolist()
                        self.w2.append(wx)
                    except:
                        pass
        else:
            for p in self.projects:
                    try:
                        wx = [p.title]+self.NEEDSrjt[self.id,p.id,:].toList()
                        self.w2.append(wx)
                    except:
                        pass

        pass
    def get3(self):
        if self.coord == 0:
            for r in self.roles:
                for p in self.people:
                        try:
                            wx = [r.title,p.fio] + self.WORKprjt[p.id,r.id, self.id, :].tolist()
                            self.w3.append(wx)
                        except:
                            pass
        else:
            for j in self.projects:
                for p in self.people:
                    try:
                        wx = [j.title,p.fio]+self.WORKprjt[p.id,self.id,j.id,:].toList()
                        self.w3.append(wx)
                    except:
                        pass

        pass
    def get4(self):
        if self.coord == 0:
            for r in self.roles:
                for p in self.people:
                        try:
                            wx = [r.title,p.fio] + self.R_W_prt[p.id,r.id, :].tolist()
                            self.w4.append(wx)
                        except:
                            pass
        else:
            for j in self.projects:
                for p in self.people:
                    try:
                        wx = [j.title,p.fio]+self.R_W_prt[p.id,self.id,:].toList()
                        self.w4.append(wx)
                    except:
                        pass
        pass
