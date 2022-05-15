from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import requests
import bs4
import datetime as dt
import json

def index(request):
    loc = '09230740'
    url = 'https://weather.naver.com/today/%s' % (loc)
    raw = requests.get(url)
    html = bs4.BeautifulSoup(raw.text, 'html.parser')
    target = html.find('ul', {'class': 'week_list'})
    day_datas = target.find_all('div', {'class': 'day_data'})
    weather_dic = {}

    for day_data in day_datas:
        date_data = day_data.find('span', {'class': 'date'})
        weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
        for weathers in weather_inner:
            timeslot = weathers.find('span', {'class': 'timeslot'})
            weather = weathers.find('i', {'class': 'ico'})
            if timeslot.text == '오전':
                weather_dic[date_data.text] = []
                weather_dic[date_data.text].append(weather.text)

    file_path = "./sample.json"
    with open(file_path, 'w') as outfile:
        json.dump(weather_dic, outfile)
    print(weather_dic)

    return render(request, 'cal/calendar.html', weather_dic)

def calendar(request):
    return render(request, 'cal/calendar.html')

def group_making(request):
    return render(request, 'cal/group_making.html')

def group_managing(request):
    return render(request, 'cal/group_managing.html')

