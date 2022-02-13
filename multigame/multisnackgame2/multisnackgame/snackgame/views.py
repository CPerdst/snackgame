from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    return render(request,'snackgame/index.html')

def getinfor(request):
    print(request.POST)
    return HttpResponse('asdasd')
def addsnack(request):
    print(request.POST)
    return HttpResponse('asdasd')