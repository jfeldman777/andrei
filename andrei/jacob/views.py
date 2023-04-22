from django.shortcuts import render
from .models import Project, UserProfile, Load, Role
import datetime
def index(request):
    return render(request, 'index.html')

def people(request):
    people = UserProfile.objects.all()
    return render(request, 'people.html', {'people': people})

def tasks(request):
    form = None
    return render(request, 'tasks.html',{form:form})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
def load(request, id):
    # Get all the items for the given ID and sort by role and month
    project = Project.objects.get(id=id)
    d1 = project.start_date
    d2 = project.end_date


    # Get the year and month of the start date and end date
    y1, m1 = d1.year, d1.month
    y2, m2 = d2.year, d2.month

    # Create a list of tuples representing the months between d1 and d2
    month_tuples = []
    while (y1, m1) <= (y2, m2):
        month_tuples.append((y1, m1))
        m1 += 1
        if m1 > 12:
            m1 = 1
            y1 += 1



    items = Load.objects.filter(project=id).order_by('role', 'month')
    print(items)
    # Create a dictionary to store the items by role and month
    items_by_role_and_month = {}

    # Loop over the items and group them by role and month
    for item in items:
        role = item.role
        month = item.month

        # If we haven't seen this role yet, create a new dictionary for it
        if role not in items_by_role_and_month:
            items_by_role_and_month[role] = {}

        # Add the item to the dictionary for this role and month
        items_by_role_and_month[role][month] = item



    # Create a list of the unique months in the data set
    months = sorted(set([item.month for item in items]))
    print(months)
    # Create a list of roles and their associated items for each month
    data = []
    for role, items_for_role in items_by_role_and_month.items():
        row = [role]
        for y,m in month_tuples:
            month = datetime.date(y,m,15)
            item = items_for_role.get(month)
            if item:
                row.append(item.load)
            else:
                row.append(0)
        data.append(row)
    print(data)

    # Pass the data to the template
    context = {'data': data, 'months': months,
               'd1':d1,'d2':d2,
               'project':project, 'month_tuples': month_tuples}
    return render(request, 'load.html', context)


