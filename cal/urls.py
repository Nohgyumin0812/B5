from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cal'
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('mycalendar/', views.mycalendar, name='mycalendar'),
    path('group_making/', views.group_making, name='group_making'),
    path('group_managing/', views.group_managing, name='group_managing'),
    path('my_schedule/', views.my_schedule, name='my_schedule'),
    path('calendar/my_schedule/', views.my_schedule, name='my_schedule'),
    path('group_recommend/', views.group_recommend, name='group_recommend'),

]
