from django.shortcuts import render

# Create your views here.
def index(request):
    data = []
    for i in range(3):
        d = []
        for j in range(5):
            d.append((i,j))
        data.append(d)
    return render(request,'index.html',{"matrix":data})

def e(request):
    return index(request)
    # return render(request,'index.html')

def index2(request):
    data = []
    for i in range(6):
        d = []
        for j in range(2):
            d.append((i,j))
        data.append(d)
    return render(request,'index.html',{"matrix":data})