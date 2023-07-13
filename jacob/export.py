import pandas as pd
from django.http import HttpResponse

from .BalanceView import BalanceView
from .models import Project  # replace with your model
from .utils import timespan_len, date0, inc
from .vvv import moon_exp, table_timeline_exp

def data_cols(mod=1):
    if mod==1:
        return ['Проект','Ресурс']+moon_exp()
    else:
        return ['Проект', 'Ресурс','Источник'] + moon_exp()

def star_date(date1,date2,d):
    if  date1 <= d <=date2:
        return '*'
    return '-'

def star_date_12(date1,date2,d,n):
    res = []
    d0 = date0()
    for i in range(n):
        star = star_date(date1,date2,d)
        res.append(star)        
        d0= inc(d0)
    return res 
    
    
def date_difference(row):
    m = timespan_len(row['start_date'], row['end_date'])
    return m

def data2page(data):
    return  pd.DataFrame(data[1:], columns=data[0])

def prj2(request):
    data = table_timeline_exp(request)
    moon = moon_exp()
    data1 = ['Название проекта','Начало','Окончание','Руководитель','Длительность (мес.)']+moon
    print(data1)
    print(data)
    df = pd.DataFrame(data, columns=data1)

    
    # Создайте HttpResponse с файлом Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Укажите имя файла
    response['Content-Disposition'] = f"attachment; filename=Doroznaya_karta.xlsx"

    # Запишите DataFrame в файл Excel
    df.to_excel(response, index=False, engine='openpyxl')


    return response
    


def prj(request):
    queryset = Project.objects.all().values('title', 'start_date', 'end_date', 'general__fio')

    # Создать DataFrame из QuerySet
    data = list(queryset)
    df = pd.DataFrame(data, columns=['general__fio','title', 'start_date', 'end_date', ])

    # Убедитесь, что поля start_date и end_date имеют формат datetime
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    

    # Применить функцию date_difference к каждой строке DataFrame (т.е., ко всем записям проекта)
    df['date_difference'] = df.apply(date_difference, axis=1)
    
    # Переименовать поля
    df = df.rename(columns={
        'title': 'Название проекта',
        'start_date': 'Начало',
        'end_date': 'Окончание',
        'general__fio': 'Руководитель',
        'date_difference':'Длительность (мес.)'
    })

    # Create a HttpResponse with an Excel file
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Name the file
    response['Content-Disposition'] = 'attachment; filename=Doroznaya_karta.xlsx'

    # Write the DataFrame to the HttpResponse
    df.to_excel(response, index=False, engine='openpyxl')

    return response

def export_plan(request,id,coord,mod):
    bv = BalanceView()    
    bv.export(request,id,coord, mod)

    data01 = data_cols(mod)
    data0 = data_cols()
    data03 = data_cols(0)
    data1 = bv.w1
    data2 = bv.w2
    data3 = bv.w3
    
    df1 = pd.DataFrame(data1, columns=data01)
    df2 = pd.DataFrame(data2, columns=data0)
    df3 = pd.DataFrame(data3, columns=data03)
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Plan.xlsx'

    # Создайте объект ExcelWriter
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df1.to_excel(writer, index=False, sheet_name='Баланс')
        df2.to_excel(writer, index=False, sheet_name='Потребность')
        df3.to_excel(writer, index=False, sheet_name='Загрузки')

    return response

def export_report(request,mod,r,y,m):
    pass
