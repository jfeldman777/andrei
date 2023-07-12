from .models import Less
from .forms import EntryForm, ProjectForm
from datetime import *
from django.shortcuts import render
from django.forms import Form
from .models import Load, Role, Project, UserProfile, Task
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .vvv import *
from typing import List, Union,Dict,Callable

from datetime import date, timedelta

'''
Всплывающая подсказка
'''
def up(a: int=-1, b: int=-1,c:str='') -> str:
    cs =  f"| {c}" if len(c.strip())>0 else ''
    bs = f" | есть: {b} " if b < 88888 else ''
    ass = f"надо: {a}"

    return ass + bs + cs

'''
Используется при тестировании для стандартизации вызова
'''
def eva2(request: object, fun: str) -> Callable:
    arguments = (request, 2, 2, 2)
    return eval(f"{fun}(*arguments)")


from django.urls import get_resolver
from django.urls import get_resolver, get_callable
from django.urls import reverse

def date0()->date:
    d = date.today().replace(day=15)
    return d


from datetime import date, timedelta
from typing import List, Dict


'''
Сдвигаем дату на 1 месяц (и относим на середину месяца)
'''
def inc(d: date) -> date:
    # Increment the input date by one month
    return (d.replace(day=15) + timedelta(days=31)).replace(day=15)  # Move to the next month's 15st day


'''
Заготовка для заголовков таблицы - 12 месяцев начиная с сегодня
'''
def mon_bar() -> List[Dict[str, int]]:
    dat: List[Dict[str, int]] = []
    d: date = date.today().replace(day=15)
    
    for i in range(12):
        dat.append({"year": d.year, "month": d.month})
        d = inc(d)

    return dat


'''
Сдвигаем дату на n месяцев
'''
def inc_n(d:date, n:int)->date:
    d1=d
    for i in range(n):
        d1 = inc(d1)
    return d1    


'''
длительность проекта в месяцах.
дата любого месяца переносится на 15е число и добавляется 1 месяц.
Проект начатый в январе и законченный в январе длится один месяц.
'''
def timespan_len(d1:date, d2:date)->int:
    return (d2.year - d1.year) * 12 + d2.month - d1.month + 1

def mon_bool_exp(dmin:date, dmax:date, dstart:date, dend:date)->List[str]:
    L = []
    d = dmin.replace(day=15)
    d2 = dmax.replace(day=15)
    d3 = dstart.replace(day=15)
    d4 = dend.replace(day=15)
    while d <= d2:
        b = d3 <= d <= d4
        star = '*' if b else ''
        L.append(star)
        d = inc(d)
        
    return L
'''
12 значений Истина-ложь для накладыванияна тайм-лайн проекта
Истина внутри сроков, Ложь - вне сроков
'''
def mon_bool(dmin:date, dmax:date, dstart:date, dend:date)->List[bool]:
    L = []
    d = dmin.replace(day=15)
    d2 = dmax.replace(day=15)
    d3 = dstart.replace(day=15)
    d4 = dend.replace(day=15)
    while d <= d2:
        b = d3 <= d <= d4
        L.append(b)
        d = inc(d)
    return L    
def mon_bool_color(dmin:date, dmax:date, dstart:date, dend:date,color1,color2)->List[bool]:
    L = []
    d = dmin.replace(day=15)
    d2 = dmax.replace(day=15)
    d3 = dstart.replace(day=15)
    d4 = dend.replace(day=15)
    while d <= d2:
        b = d3 <= d <= d4

        if b:
            x = {"val":"*","color":color1,"align":"center"}
        else:
            x = {"val": " ", "color": color2,"align":"center"}
        L.append(x)
        d = inc(d)
    return L
'''
за сколько месяцев
'''
def n2txt(n:int)->str:
    if n == 1:
        return "на 1 месяц"
    if n == 3:
        return "на 3 месяца"
    return f"на {n} месяцев"


'''
месяц вне проекта - да или нет
'''
def mon_outside_prj(m:date, j:Project)->bool:
    if j == None:
        return True
    d1 = j.start_date
    d2 = j.end_date
    return not (d1 <= m and m <= d2)

