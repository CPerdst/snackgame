from unicodedata import name
from django.urls import path
from . import views

app_name='snackgame'
urlpatterns=[
    path('',views.index,name='index'),
    path('getinfor/',views.getinfor,name='getinfor'),
    path('addsnack/',views.addsnack,name='addsnack'),
]