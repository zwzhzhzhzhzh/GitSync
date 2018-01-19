from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import View

from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    context={}
    context['hello']='Hello World!'
    return render(request,'hello.html',context)
    #return HttpResponse("Hello World!")

def chart(request):
    return render(request,'charts.html')
    #return HttpResponse("Hello World!")

User = get_user_model()

def HomeView(request):
    return render(request, 'charts.html', {"customers": 10})



def get_data(request):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response



def ChartData(request):
    qs_count = User.objects.all().count()
    labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
    default_items = [qs_count, 23, 2, 3, 12, 2]
    data = {
            "labels": labels,
            "default": default_items,
    }
    return HttpResponse(data)
