from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .db import get_prj_triplet, task_role_project_12, delta_role_project_12, needs_role_project_12, \
    real_people, real_and_virtual_people, rest_of_time_pr_12, task_person_role_project_12, rest_and_color_12, \
    rest_role_12
from .models import Project,Role,Wish,Grade

from .paint import Paint
from .utils import date0, inc, up
from  .vvv import moon, outsrc, vacancia
class BalanceView(View):
    def __init__(self):
        self.w1 = []
        self.w2 = []
        self.w3 = []
        self.w4 = []
        self.paint1 = Paint()
        self.paint2 = Paint()
        self.flag = True
        return

    def get(self, request,id,coord=0, mod=0,n=12):
        self.n = n
        self.mod = mod
        self.coord = coord
        self.id = id

        moon12 = moon()

        if coord == 0:
            project = Project.objects.get(id=id)
            roles = Role.objects.all().order_by('title')
            for role in roles:
                self.get_1(project,role)


        else:
            projects = Project.objects.all().order_by('title')
            role = Role.objects.get(id=id)
            for project in projects:
                self.get_1(project,role)

        moon12["w1"] = self.w1
        moon12["w2"] = self.w2
        moon12["w3"] = self.w3
        moon12["w4"] = self.w4

        moon12["role"] = role

        moon12["project"] = project
        moon12["id"] = id
        moon12["r"] = role.id
        moon12["j"] = project.id

        moon12["p"] = 0
        moon12['is_delta'] = self.mod == 1
        moon12['mod'] = self.mod
        moon12['coord'] = self.coord
        moon12['pp'] = project.title if coord == 0 else role.title
        moon12['res_or_prj'] = "Ресурс" if coord == 0 else "Проект"
        moon12['prj_bool'] = self.coord == 0
        print(67676,self.coord == 0)

        if coord == 0:
            moon12['project_name']=project.title
            moon12['role_name']="все ресурсы"
        else:
            moon12['role_name']=role.title
            moon12['project_name']="все проекты"

        if self.mod < 2:
            return render(request, "balance_4.html", moon12)
        elif self.mod == 3:
            return render(request, "balance_2_workload.html", moon12)
        else:
            return render(request, "balance_1_needs.html", moon12)
    def get_1(self,project,role):
        zo = None
        zv = None
        supp = None
        delta = None


        #self.paint1.next_row(None)
        self.paint2.next_row(None)
        delta = delta_role_project_12(role, project, self.n)
        if self.mod == 0:
            zo = ["АУТСОРС"] + outsrc(role, project,self.n)
            zv = ["ВАКАНСИЯ"] + vacancia(role, project,self.n)
            supp = ["Поставка"] + task_role_project_12(role, project,self.n)


        dem_rj = needs_role_project_12(0,role, project,self.n)
        try:
            wish = Wish.objects.get(project=project, role=role).mywish
        except:
            wish = ''

        pp2 = project.title if self.coord == 1 else role.title

        if self.mod != 3:
                d = date0()
                a_w2 = [0] * self.n
                rest = rest_role_12(role,self.n)
                k = 0
                for i in range(self.n):
                    k = 1 - k
                    self.paint2.next_cell(dem_rj[i])

                    a_w2[i] = {
                        "link": f"0.{role.id}.{project.id}.{d.year}-{d.month}-15",
                        "val": dem_rj[i],
                        "color": self.paint2.color_needs(project.start_date, project.end_date, d ),
                        "class": " good",
                        "up":up(max(-delta[i], 0), rest[i],wish),
                    }  #
                    d = inc(d)
                wish_sign = ' !' if wish != '' else ''
                self.w2.append([{"class":"even" if k==0 else "odd",
                                 "up":wish,
                                 "color":self.paint2.rgb_back_left(),
                                 "val": pp2 + wish_sign,

                            "project": project.id, "role": role.id, "class":"wish",
                            }] + a_w2)


        people_rr = real_people(role)
        people_rv = real_and_virtual_people(role)
        if self.coord == 0:
            p4 = pp2
        else:
            p4=-1
        p3 = pp2
        paint4 = Paint()
        paint3 = Paint()

        if self.flag:
            for person in people_rr:
                paint4.next_row(None)
                dif = [{"color": paint4.rgb_back_left(),"align":"left",
                        "val": add_grade(person,role)}] + rest_and_color_12(person, role, paint4.color_rest,False ,12)
                if self.coord==0:
                    self.w4.append([p4] + dif)
                else:
                    self.w4.append(dif)
                    self.flag = False
                p4 = -1

        if self.mod !=2:
            k=0
            for person in people_rv:  #
                k=1-k
                paint3.next_row(None)

                diff = rest_of_time_pr_12(person, role,self.n)
                b_w3 = [0] * self.n
                a_w3 = task_person_role_project_12(person, role, project,self.n)

                d = date0()
                for i in range(self.n):
                    paint3.next_cell(a_w3[i])
                    isOut = d < project.start_date.replace(day=15) or d > project.end_date.replace(day=15)
                    isPurple = delta[i] < 0
                    b_w3[i] = {
                        "link": f"{person.id}.{role.id}.{project.id}.{d.year}-{d.month}-15",
                        "up": up(max(-delta[i], 0), diff[i],wish),
                        "val": a_w3[i],
                        "color": paint3.color_tasks(isOut,isPurple),
                        "class": "  good",
                        "align":"center"
                    }
                    d = inc(d)

                    c_w3 = [{"val":p3,'class': "even" if k==0 else "odd"},{"align":"left",
                                        "val": add_grade(person,role)}] + b_w3

                if self.mod < 2:
                    p3 = -1
                self.w3.append(c_w3)

        if self.coord == 1 :
            p1 = project.title
        else:
            p1 = role.title

        if self.mod == 0:
            self.w1.append([p1]+self.paint1.plus_color_balance(  ["Потребность"] + dem_rj) ) ##########################################77777
            self.paint1.next_row(None)
            self.w1.append([-1] + self.paint1.plus_color_balance(supp) ) ###############--
            self.paint1.next_row(None)
            self.w1.append([-1] + self.paint1.plus_color_balance(zo))  ################
            self.paint1.next_row(None)
            self.w1.append([-1] + self.paint1.plus_color_balance(zv) ) #####################
            delta = ["Дельта"] + delta

        self.paint1.next_row(None)
        self.w1.append([-1] + self.paint1.plus_color_balance(delta,self.mod == 0) ) ############################

        return


def add_grade(person,role):
    up1 = ''
    if not person.virtual:
        try:
            grade = Grade.objects.get(person=person, role=role).mygrade
        except:
            grade = '0'
        up1 = f" ({grade})"
    return person.fio + up1