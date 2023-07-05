from django.shortcuts import render


def view1(request):
    # Assuming your data is a list of numbers
    data = [1, 2, 3, 4, 5, 6, 7, 7, 7, 8, 9, 9]
    return render(request, 'gisto.html', {'data': data})
