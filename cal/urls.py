from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cal'
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
	path('event/edit/int:event_id/', views.event, name='event_edit'),
    path('login', auth_views.LoginView.as_view(template_name ='cal/login.html'), name ='login'), #  임시로 작성
    path('signup/', views.signup, name ='signup'),
    path('group_making/', views.group_making, name='group_making'),
    path('group_managing/', views.group_managing, name='group_managing'),

]
