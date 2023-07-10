from django.shortcuts import render
from django.views import View
import numpy as np

from .BalanceView import minus, my_red, add_grade
from .paint import Paint
from .utils import  date0, up, inc_n
from .models import UserProfile, Project, Role, Less, Load, Task, Wish
from django.db.models import Max
from .timing import timing_decorator
from .vvv import moon




def timespan_dif(d1, d2):
    dx = (d2.year - d1.year) * 12 + d2.month - d1.month
    return dx

def time_n(d):
    res = timespan_dif(date0(),d)
    return res

class BalanceNum(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []

        self.paint1 = Paint()
        self.paint2 = Paint()
        self.paint3 = Paint()
        self.paint4 = Paint()


        self.OUTSRC = UserProfile.objects.get(fio='АУТСОРС')
        self.VACANCY = UserProfile.objects.get(fio='ВАКАНСИЯ')

        self.nProject = Project.objects.all().aggregate(Max('id'))['id__max']+1
        self.nRole = Role.objects.all().aggregate(Max('id'))['id__max']+1
        self.nPerson = UserProfile.objects.all().aggregate(Max('id'))['id__max']+1
        self.people = list(UserProfile.objects.exclude(virtual=True).order_by('fio'))
        
        print(899,self.people)

        self.people_rv = self.people + [self.OUTSRC,self.VACANCY]
        self.nTime = 12

        self.wish = Wish.objects.all()
        self.my_wish = dict()
        for w in self.wish:
            self.my_wish[f"{w.role}.{w.project}"]=w.mywish
        return

    def get_wish(self,role,project):
        key = f"{role}.{project}"
        val = ""
        try:
            val = self.my_wish[key]
        except:
            pass
        return val


    @timing_decorator
    def get(self,request,id,coord,mod):
        moon12 = moon()
        self.init(id,coord,mod)
        if mod < 3:
            self.get2()
        
        if mod == 0:
            self.get1()
            
        elif mod==1:
            self.get1delta()
            
        if mod != 2: 
            self.get3()
        if mod < 2:
            self.get4()
            
        moon12['w1'] = self.w1
        moon12['w2'] = self.w2
        moon12['w3'] = self.w3
        moon12['w4'] = self.w4
        moon12['is_delta'] = self.mod == 1
        moon12['mod'] = self.mod
        moon12['id'] = self.id
        moon12['coord'] = self.coord
        moon12['pp'] = self.title
        moon12['res_or_prj'] = "Ресурс" if coord == 0 else "Проект"
        moon12['prj_bool'] = self.coord == 0


        if coord == 0:
            moon12['project_name']=self.title
            moon12['role_name']="все ресурсы"
        else:
            moon12['role_name']=self.title
            moon12['project_name']=" все проекты"

        if self.mod < 2:
            return render(request, "balance_4.html", moon12)
        elif self.mod == 3:
            return render(request, "balance_2_workload.html", moon12)
        else:
            return render(request, "balance_1_needs.html", moon12)


    def setAVLprt(self):
        if self.coord == 1:
            avls = Less.objects.filter(role=self.id)
        else:
            avls = Less.objects.all()
        self.avls=avls
        for a in avls:
            p = a.person
            r = a.role
            if r.id == p.role.id or r.id in set(p.res.values_list('id', flat=True)):
                    t = time_n(a.start_date)   #-1
                    self.AVLprt[p.id,r.id,t]=a.load

        try:
            print(self.people,self.roles)
            for p in self.people:                
                for r in self.roles:
                    try:
                        st = set(p.res.values_list('id', flat=True))
                    except :
                        st = []
                    try:
                        if r.id == p.role.id or r.id in st:
                            for t in range(self.nTime):
                                if self.AVLprt[p.id,r.id,t]==0:
                                    if t == 0 and p.role.id == r.id:
                                        self.AVLprt[p.id,r.id,t]=100
                                    else:
                                        self.AVLprt[p.id, r.id,t] = self.AVLprt[p.id,r.id,t-1]
                    except:
                        pass

        except:
            print(p,r,t,900)

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
                if t >= 0:
                    try:
                        self.NEEDSrjt[r,j,t]=a.load
                    except:
                        print(r,j,800)
            except:
                print(a,700)
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

    def set_R_W_rt(self):
        self.R_W_rt = np.sum(self.R_W_prt, axis=0)


    def set_N_W_rjt(self):
            self.N_W_rjt = self.NEEDSrjt.copy()
            for r in self.roles:
                for t in range(self.nTime):
                    for j in self.projects:
                        for p in self.people_rv:
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
            self.projects = [Project.objects.get(id = self.id)]
            self.roles = Role.objects.all().order_by('title')
        else:
            self.roles = [Role.objects.get(id=self.id)]
            self.projects = Project.objects.all().order_by('title')

        self.title = self.projects[0].title if coord == 0 else self.roles[0].title

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
        self.set_R_W_rt()

        self.set_N_W_rjt()
        self.set_PRJtime()

        return
    
    def get1of5(self,title,n):
        self.paint4.next_row()
        title0 = self.get0title(n)
        res = 
            [{"val":title0,"color":self.paint1.rgb_back_left()},
            {"val":title,"color":self.paint1.rgb_back_right()}]
        return res

    def get0title(self,n):
        if n == 1:
            return 'Потребность'
        if n == 2:
            return 'Поставка'
        if n == 3:
            return 'АУТСОРС'
        if n == 4:
            return 'ВАКАНСИЯ'
        if n == 5:
            return 'Дельта'
        return "error"

    def get1right(self,role,project):
        res = []
        for t in range(self.nTime):
            self.paint1.next_cell(int(-self.N_W_rjt[role.id,project.id,t]))
            res.append(
                {
                    'val':-self.N_W_rjt[role.id,project.id,t],
                        'color':self.paint1.color_balance_new()
                }

            )
        return res

    
    
    def get1(self):
        if self.coord == 0:
            j = self.projects[0]
            for r in self.roles:
                title = r.title
                self.paint1.next_row()
                
                try:
                        wx = [self.get1left(title,1)] + self.get1right1(r,j)
                        self.w1.append(wx)
                        wx = [self.get1left(title,2)] + self.get1right2(r,j)
                        self.w1.append(wx)
                        wx = [self.get1left(title,3)] + self.get1right3(r,j)
                        self.w1.append(wx)
                        wx = [self.get1left(title,4)] + self.get1right4(r,j)
                        self.w1.append(wx)
                        wx = [self.get1left(title,5)] + self.get1right(r,j)
                        self.w1.append(wx)
                except:
                        pass

        else:
            r = self.roles[0]
            for j in self.projects:                
                    title = j.title
                    self.paint1.next_row()
                    
                    try:
                        wx = [self.get1left(title)] + self.get1right(r,j)
                        self.w1.append(wx)
                    except:
                        pass
                    
        return
    
    def get1right1(self,r,j):
        return []
    
    def get1right2(self,r,j):
        return []
    
    def get1right3(self,r,j):
        return []
    
    def get1right4(self,r,j):
        return []
    
    
    def get1delta(self):
        if self.coord == 0:
            j = self.projects[0]
            for r in self.roles:
                title = r.title
                self.paint1.next_row()
                try:
                        wx = [self.get1leftDelta(title)] + self.get1right(r,j)
                        self.w1.append(wx)
                except:
                        pass

        else:
            r = self.roles[0]
            for j in self.projects:
                    title = j.title
                    self.paint1.next_row()
                    try:
                        wx = [self.get1leftDelta(title)] + self.get1right(r,j)
                        self.w1.append(wx)
                    except:
                        pass
        return

    def get2(self):
        if self.coord == 0:
            k=0
            for r in self.roles:
                k = 1-k
                self.paint2.next_row()
                try:
                    j = self.projects[0]
                    wx1 = self.get2left(r,j,k)
                    wx2 = self.get2right(r,j)
                    self.w2.append([wx1] + wx2)
                except:
                    pass
        else:
            k=0
            for j in self.projects:
                k = 1-k
                self.paint2.next_row()
                try:
                    r = self.roles[0]
                    wx = [self.get2left(r,j,k)] + self.get2right(r,j)
                    self.w2.append(wx)
                except:
                    pass

        pass
    def get_wish_sign(self,role,project):
        wish = self.get_wish(role,project)
        ws = ' !' if wish != '' else ''
        return ws

    def get2left(self,role,project,k):
        title = project.title if self.coord == 1 else role.title
        wsh = self.get_wish_sign(role,project)
        wx = {"class": "even" if k == 0 else "odd",
                         "up": self.get_wish(role,project),
                         "color": self.paint2.rgb_back_left(),
                         "val": title + wsh,
                         "project": project.id,
                         "role": role.id,
                         "class": "wish",
                         }
        return wx


    def d2s(self,n):
        d0 = date0()
        d = inc_n(d0,n)
        s = f"{d.year}-{d.month}-15"
        return s

    def get2right(self,role,project):
        res = []
        for t in range(self.nTime):
           ds = self.d2s(t)
           self.paint2.next_cell(int(self.NEEDSrjt[role.id,project.id,t]))
           res.append(
               {  "link": f"0.{role.id}.{project.id}.{ds}",
                    "val": self.NEEDSrjt[role.id,project.id,t],
                    "color": self.paint2.color_needs_n(project.start_date, project.end_date, t),
                    "class": " good",
                    "up": up(
                        max(-self.N_W_rjt[role.id,project.id,t], 0),
                             self.R_W_rt[role.id,t],
                             self.get_wish(role,project)
                    ),
                })
        return res

    def get3right(self,person,role,project):
        res = []
        for t in range(self.nTime):
            cell = self.WORKprjt[person.id,role.id,project.id,t]
            self.paint3.next_cell(cell)
            res.append(
            {"workload": True,
         "link": f"{person.id}.{role.id}.{project.id}.{self.d2s(t)}",
         "up": up(max(-self.N_W_rjt[role.id,project.id,t], 0),
                  self.R_W_prt[person.id,role.id,t], self.get_wish(role,project)),
         "val": minus(self.WORKprjt[person.id,role.id,project.id,t],
                      self.R_W_prt[person.id,role.id,t]),
         "color": self.paint3.color_workload(self.PRJtime[project.id,t],
                                             -self.N_W_rjt[role.id,project.id,t], False),
         "tcolor": my_red(cell,
                          self.R_W_prt[person.id,role.id,t]),
         "class": "  good",
         "align": "center"
         })

        return res

    def get3left(self,person,role,project,title,k):
        res =  [{"val": title, 'class': "even" if k == 0 else "odd",

          }, {"align": "left", "color": "" if self.mod == 3 else self.paint3.rgb_back_left(),
              "val": add_grade(person, role)}]
        return res

    def get3(self):
        if self.coord == 0:
            j = self.projects[0]
            for r in self.roles:
                title = r.title
                k = 0
                self.paint3.next_row()
                for p in self.people_rv:
                    try:
                        if r.id == p.role.id or r.id in set(p.res.values_list('id', flat=True)) \
                                or p.fio in ['ВАКАНСИЯ','АУТСОРС']:
                            k = 1-k
                            try:
                                wx = self.get3left(p,r,j,title,k) + self.get3right(p,r,j)
                                self.w3.append(wx)
                                title = -1
                            except:
                                pass
                    except:
                        pass
        else:
            r = self.roles[0]
            for j in self.projects:
                title = j.title
                k = 0
                self.paint3.next_row()
                for p in self.people_rv:
                    try:
                        if r.id == p.role.id or r.id in set(p.res.values_list('id', flat=True))  or \
                                p.fio in ['ВАКАНСИЯ','АУТСОРС']:
                            k = 1 - k
                            try:
                                wx = self.get3left(p, r, j, title, k) + self.get3right(p, r, j)
                                self.w3.append(wx)
                                title = -1
                            except:
                                pass
                    except:
                        pass
        return

    def get4(self):
        if self.coord == 0:
            for r in self.roles:
                title = r.title
                k = 0
                for p in self.people:
                    try:
                        if r.id == p.role.id or r.id in set(p.res.values_list('id', flat=True)) :
                            print(676,p,r)
                            k = 1 - k
                            self.paint4.next_row()
                            try:
                                wx = [title]+self.get4left(p,r)+self.get4right(p,r)
                                self.w4.append(wx)
                                title = -1
                            except:
                                pass
                    except:
                        pass
        else:
                r = self.roles[0]
                k = 0
                for p in self.people:
                    try:
                        if r.id == p.role.id or r.id in set(p.res.values_list('id', flat=True)):
                            k = 1 - k
                            self.paint4.next_row()
                            try:
                                wx = self.get4left(p,r)+self.get4right(p,r)
                                self.w4.append(wx)
                            except:
                                pass
                    except:
                        pass
        pass

    def get4left(self,person,role):
        res = [{"color": self.paint4.rgb_back_left(), "align": "left",
         "val": add_grade(person, role)}]
        return res

    def get4right(self,person,role,is_1=False):
        c = self.R_W_prt[person.id, role.id]
        res = []
        for t in range(self.nTime):
            self.paint4.next_cell(c[t])
            res.append({"val": c[t],
                        "align": "center",
                "color": self.paint4.color_rest(c[t], is_1)})

        return res