import pandas as pd
from django.http import HttpResponse

from .BalanceView import BalanceView
from .models import Project  # replace with your model
from .utils import timespan_len, date0, inc
from .vvv import moon_exp, table_timeline_exp


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

def export_plan(request):
    # Создайте HttpResponse
    from django.http import HttpResponse
    import pandas as pd
    bv = BalanceView()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Plan.xlsx'

    # Создайте объект ExcelWriter
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        # Предположим у вас есть два QuerySet
        # queryset1 = Project.objects.all().values('title', 'start_date', 'end_date', 'general__fio')
        # queryset2 = AnotherModel.objects.all().values('field1', 'field2')
        # queryset3 = AnotherModel.objects.all().values('field1', 'field2')
        # queryset4 = AnotherModel.objects.all().values('field1', 'field2')

        # # Создайте DataFrame из QuerySet
        # df1 = pd.DataFrame(list(queryset1))
        # df2 = pd.DataFrame(list(queryset2))
        # df3 = pd.DataFrame(list(queryset3))
        # df4 = pd.DataFrame(list(queryset4))


        ex3 = bv.export_3()
        df3 = data2page(ex3)

        # Запишите DataFrame в разные листы
        # df1.to_excel(writer, index=False, sheet_name='баланс>')
        # df2.to_excel(writer, index=False, sheet_name='Потребность')
        # df3.to_excel(writer, index=False, sheet_name='Загрузки')


    # В результате у вас будет Excel-файл с двумя вкладками: Sheet1 и Sheet2
    import pandas as pd
    from django.http import HttpResponse

    # Предположим, у вас есть список словарей:
    data = [
        {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'},
        {'field1': 'value4', 'field2': 'value5', 'field3': 'value6'},
        # и т.д.
    ]

    # Создайте DataFrame из списка словарей
    df = pd.DataFrame(data)

    # Создайте HttpResponse с файлом Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Укажите имя файла
    response['Content-Disposition'] = 'attachment; filename=Export.xlsx'

    # Запишите DataFrame в файл Excel
    df.to_excel(response, index=False, engine='openpyxl')

    # В результате у вас будет файл Excel, в котором каждый словарь представлен одной строкой,
    # а ключи словаря становятся именами столбцов.
    import pandas as pd
    from django.http import HttpResponse

    # Предположим, у вас есть список списков следующего вида:
    data = [
        ['column1', 'column2', 'column3'],  # имена столбцов
        ['value1', 'value2', 'value3'],  # значения первой строки
        ['value4', 'value5', 'value6'],  # значения второй строки
        # и т.д.
    ]

    # Создайте DataFrame из списка списков, используя первый список как имена столбцов
    df = pd.DataFrame(data[1:], columns=data[0])

    # Создайте HttpResponse с файлом Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Укажите имя файла
    response['Content-Disposition'] = 'attachment; filename=Export.xlsx'

    # Запишите DataFrame в файл Excel
    df.to_excel(response, index=False, engine='openpyxl')

    # В итоге у вас будет файл Excel, где каждый список представлен одной строкой,
    # а элементы первого списка используются в качестве имен столбцов.

