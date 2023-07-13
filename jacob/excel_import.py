import pandas as pd
from .models import Project, UserProfile

from django.shortcuts import render
from .forms import UploadFileForm
from .models import Project, UserProfile
import pandas as pd

def upload(request,mod):
    if mod == 1:
        return prj_import(request)
    return staff_import(request)

def staff_import(request):
    if request.method == 'POST':
        protocol = []
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                fio = row['fio']

                try:
                    person0 = UserProfile.objects.filter(fio = fio)[0]
                    protocol.append(f"Это сотрудник уже есть в базе: {fio}")
                except:
                    pass


                # UserProfile = Project(
                #     title=title,
                #     start_date=pd.to_datetime(start_date),
                #     end_date=pd.to_datetime(end_date),
                #     general=general,
                # )
                # project.save()

            return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form,"mod":2,"title":'Импорт сотрудников'})

def prj_import(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                title = row['title']
                start_date = row['start_date']
                end_date = row['end_date']
                general_id = row['general']
                general = UserProfile.objects.get(id=general_id)

                project = Project(
                    title=title,
                    start_date=pd.to_datetime(start_date),
                    end_date=pd.to_datetime(end_date),
                    general=general,
                )
                project.save()

            return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form,"mod":1,"title":'Импорт проектов'})


def go_import_prj():
        # Read Excel file
        df = pd.read_excel('path_to_your_excel_file.xlsx')

        # Iterate over each row in the DataFrame (which represents a row in the Excel data)
        for index, row in df.iterrows():
            # Assuming Excel columns are named the same as your model fields
            title = row['title']
            start_date = row['start_date']
            end_date = row['end_date']

            # Assuming there's a column 'general' which contains user's id
            general_fio = row['general']
            try:
                general = UserProfile.objects.get(fio=general_fio)
            except:
                general = UserProfile.objects.get(user='admin')


            project = Project(
                title=title,
                start_date=pd.to_datetime(start_date),  # convert string to datetime
                end_date=pd.to_datetime(end_date),
                general=general,
            )
            project.save()

            # # Assuming there's a column 'people' which contains comma separated user's ids
            # people_ids = row['people'].split(',')
            # for person_id in people_ids:
            #     person = UserProfile.objects.get(id=int(person_id))
            #     project.people.add(person)


def project_import(request):
    return prj_import(request)

def person_import(request):
    return staff_import(request)