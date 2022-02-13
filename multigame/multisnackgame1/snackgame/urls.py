from django.urls import URLPattern, path,include
from . import views
app_name='snackgame'
urlpatterns=[
    path('snackgame/',view=views.index,name='snackgame'),
]