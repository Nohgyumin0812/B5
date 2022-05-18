import json

import bs4
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import GroupForm
from .models import CustomGroup


def index(request):
    return render(request, 'common/login.html')


@login_required()
def calendar(request):
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
                # weather_dic[date_data.text] = []
                # weather_dic[date_data.text].append(weather.text)
                weather_dic[date_data.text] = weather.text


    file_path = "./sample.json"
    with open(file_path, 'w') as outfile:
        json.dump(weather_dic, outfile, ensure_ascii=False)
    data = json.dumps(weather_dic, ensure_ascii=False)
    print(data)
    return render(request, 'cal/calendar.html', {'data': data})


@login_required()
def group_making(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        print(request.POST)
        # owner = request.username

        if form.is_valid():
            group = form.save(commit=False)
            print('##################')
            group.owner = request.user
            group.group_name = request.POST["groupname"]
            group.sports = request.POST.getlist('sports')
            group.friendname = request.POST.getlist("friendname")
            print(group.friendname)
            group.save()
            return redirect('cal:group_managing')
    return render(request, 'cal/group_making.html')


def group_managing(request):
    return render(request, 'cal/group_managing.html')

