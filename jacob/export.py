import pandas as pd
from django.http import HttpResponse
from .models import Project  # replace with your model
from .utils import timespan_len


def date_difference(row):
    m = timespan_len(row['start_date'], row['end_date'])
    return m


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
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Укажите имя файла
    response['Content-Disposition'] = 'attachment; filename=Plan.xlsx'

    # Создайте объект ExcelWriter
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        # Предположим у вас есть два QuerySet
        queryset1 = Project.objects.all().values('title', 'start_date', 'end_date', 'general__fio')
        queryset2 = AnotherModel.objects.all().values('field1', 'field2')
        queryset3 = AnotherModel.objects.all().values('field1', 'field2')
        queryset4 = AnotherModel.objects.all().values('field1', 'field2')

        # Создайте DataFrame из QuerySet
        df1 = pd.DataFrame(list(queryset1))
        df2 = pd.DataFrame(list(queryset2))
        df3 = pd.DataFrame(list(queryset3))
        df4 = pd.DataFrame(list(queryset4))

        # Запишите DataFrame в разные листы
        df1.to_excel(writer, index=False, sheet_name='Sheet1')
        df2.to_excel(writer, index=False, sheet_name='Sheet2')
        df3.to_excel(writer, index=False, sheet_name='Sheet3')
        df4.to_excel(writer, index=False, sheet_name='Sheet4')

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
