from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cal'
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calender'),
    path('group_making/', views.group_making, name='group_making'),
    path('group_managing/', views.group_managing, name='group_managing'),
    path('calendar/my_schedule/', views.my_schedule, name='my_schedule'),

]
