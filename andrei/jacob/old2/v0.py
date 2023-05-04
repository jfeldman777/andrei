#
# def table_formset_view(request):
#     table = []
#     # Replace with your own method of obtaining table data
#     formset = table_to_formset(table)
#     if request.method == 'POST':
#         formset = TableCellForm(request.POST)
#         if formset.is_valid():
#             # Handle form submission
#             pass
#     return render(request, 'table_formset.html', {'formset': formset})
#
# def res2(request,prj,role,y,m):
#     project = Project.objects.get(id=prj)
#     people = project.people.filter(role = role)
#
#     initial_data = []
#     for user in people:
#         loads = Task.objects.filter(role=role, project=prj, month=f"{y}-{m}-15")
#         initial_data.append({"role": role.id, 'project': prj,
#                              "month": f"{y}-{m}-15","person":user.id,
#                              "label": user.last_name})
#         if loads:
#             initial_data.append({"load": loads[0].load,})
#
#     LoadFormSet = formset_factory(CellForm, extra=0)
#     if request.method == "POST":
#         formset = LoadFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 role_id = form.cleaned_data["role"]
#                 load = form.cleaned_data["load"]
#                 person = form.cleaned_data["person"]
#                 Task.objects.update_or_create(
#                    role_id=role_id, project=project, month=f"{y}-{m}-15", defaults={"load": load},
#                    person = person
#                 )
#         else:
#             print(formset.errors)
#         return redirect("res", prj)
#     else:
#         formset = LoadFormSet(initial=initial_data)
#     context = {"formset": formset, "project": project, "month": f"{y}-{m}", }
#     return render(request, "res2.html", context)