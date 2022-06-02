import json
from urllib import parse
from urllib.parse import unquote, quote, quote_plus, urlencode
import bs4
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import ast
from .forms import GroupForm, DayForm, DaysForm
from .models import CustomGroup, DayGroup, DaysGroup
from common.models import CustomUser
from django.contrib.auth.models import Group
import pandas as pd

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
    sports_dic = {}
    indoor_sports = ['3', '4', '6']
    outdoor_sports = ['1', '2', '5']
    curr_url = parse.unquote(str(request.build_absolute_uri()))
    curr_url = curr_url.split('/')

    print(curr_url)
    if curr_url[4] == '':
        return render(request, 'cal/mycalendar.html')



    curr_group = (curr_url[4]).replace('?', '')
    print(curr_group)
    try:
        ## 그룹 종목 출력 ##
        sportsall = CustomGroup.objects.get(groupname=curr_group).sports
        sportsall = ast.literal_eval(sportsall)
        sports = json.dumps(sportsall, ensure_ascii=False)

        ## 날씨 크롤링 ##
        for day_data in day_datas:
            date_data = day_data.find('span', {'class': 'date'})
            weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
            print(weather_inner)
            for weathers in weather_inner:
                timeslot = weathers.find('span', {'class': 'timeslot'})
                weather = weathers.find('i', {'class': 'ico'})

                if timeslot.text == '오전':
                    #weather_dic[date_data.text] = []
                    # weather_dic[date_data.text].append(weather.text)
                    weather_dic[date_data.text] = weather.text

                    if weather.text == '흐리고 비'or weather.text == '비 또는 눈' or weather.text ==  '눈 또는 비' or weather.text == '가끔 비 또는 눈' \
                            or weather.text == '한때 비 또는 눈' or weather.text == '가끔 눈 또는 비' or weather.text == '한때 눈 또는 비' or \
                            weather.text == '안개' or weather.text == '연무' or weather.text == '박무 (엷은 안개)' or weather.text == '빗방울' \
                            or weather.text == '눈날림' or weather.text == '낙뢰' or weather.text == '황사' or weather.text == '비' or weather.text == '눈':
                        sports_dic[date_data.text] = list(set(sportsall) & set(indoor_sports))
                    elif weather.text == weather.text == '맑음' or weather.text == '구름많음' or weather.text == '구름조금' or weather.text == '흐림':
                        sports_dic[date_data.text] = list(set(sportsall) & set(outdoor_sports))

    # file_path = "./sample.json"
    # with open(file_path, 'w') as outfile:
    #     json.dump(weather_dic, outfile, ensure_ascii=False)
        data = json.dumps(weather_dic, ensure_ascii=False)
        sports_date = json.dumps(sports_dic, ensure_ascii=False)


    ## 그룹 참여자 출력 ##
        owner = CustomGroup.objects.get(groupname=curr_group).owner.username
        member = CustomGroup.objects.get(groupname=curr_group).friendname
        member = ast.literal_eval(member)
        if '' in member:
            member.remove('')
        membersall = [owner]+ member
        members = json.dumps(membersall, ensure_ascii=False)

        request.session['data'] = data
        request.session['sports'] = sports
        request.session['members'] = members
        request.session['sports_date'] = sports_date
        request.session['curr_group'] = curr_group

        my_group_id = CustomGroup.objects.get(groupname=curr_group).id
        print(my_group_id)
        schedule_data = DayGroup.objects.filter(group_id=my_group_id).values_list()
        schedule_data = pd.DataFrame(schedule_data)
        try:
            schedule_data = schedule_data[schedule_data.iloc[:, 1] == my_group_id].iloc[:, 2]
            schedule_data_lst = []
            for i in range(schedule_data.shape[0]):
                schedule_data_lst += schedule_data[i].split(",")
        except:
            schedule_data_lst = []

        schedule_data_lst = list(set(schedule_data_lst))
        print(schedule_data_lst)
        schedule_data_lst = json.dumps(schedule_data_lst, ensure_ascii= False)

        context = {'data': data, 'sportsall':sports, 'membersall':members, 'sports_date':sports_date, 'schedule_data_lst':schedule_data_lst}
        return render(request, 'cal/calendar.html', context)
    except CustomGroup.DoesNotExist:
        return render(request, 'cal/group_making.html')





@login_required()
def group_making(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        print(form)
        if form.is_valid():
            print("$$")
            group = form.save(commit=False)
            group.owner = request.user
            group.group_name = request.POST["groupname"]
            group.sports = request.POST.getlist('sports')
            group.friendname = request.POST.getlist("friendname")

            group.save()
            return redirect('cal:group_managing')
    return render(request, 'cal/group_making.html')

#2015
#00016

@login_required()
def group_managing(request):
    my_group = []
    group = CustomGroup.objects.all().values()
    user = CustomUser.objects.all().values()
    username = CustomUser.objects.get(id=request.user.id).username

    df = pd.DataFrame(group)
    df_user = pd.DataFrame(user)
    df_group = (pd.DataFrame(df[['groupname','owner_id', 'friendname']]))

    df_user['owner_id']= df_user['id']
    df_user = (df_user[['owner_id', 'username']])
    df_inner_join = pd.merge(df_group, df_user, left_on = 'owner_id', right_on = 'owner_id', how = 'inner')
    #print(df_user[df_user['id'] == df['owner_id']])
    for i in range(df_inner_join.shape[0]):
        df_inner_join['username'][i] = [df_inner_join['username'][i]]
        df_inner_join['friendname'][i] = ast.literal_eval(df_inner_join['friendname'][i])+(df_inner_join['username'][i])
        if username in df_inner_join['friendname'][i]:
            my_group.append(df_inner_join['groupname'][i])
    print(my_group)
    group_json = json.dumps(my_group, ensure_ascii=False)

    return render(request, 'cal/group_managing.html', {'my_group':my_group})

def my_schedule(request):
    schedule_data = []
    data = request.session['data']
    sports = request.session['sports']
    members = request.session['members']
    sports_date = request.session['sports_date']
    curr_group = request.session['curr_group']
    my_group_id = CustomGroup.objects.get(groupname = curr_group ).id
    print(my_group_id)
    #my_schedule 데이터 전송 확인 부분
    if request.method == 'POST':
        schedule_data = request.POST["myDates"]

        form = DayForm(request.POST)
        if form.is_valid():
            Day = form.save(commit=False)
            Day.group_id = CustomGroup.objects.get(groupname = curr_group ).id
            Day.dates = schedule_data
            Day = form.save()

    schedule_data = DayGroup.objects.filter(group_id = my_group_id).values_list()
    schedule_data = pd.DataFrame(schedule_data)
    try:
        schedule_data = schedule_data[schedule_data.iloc[:, 1] == my_group_id].iloc[:, 2]
        schedule_data_lst = []

        for i in range(schedule_data.shape[0]):
            schedule_data_lst += schedule_data[i].split(",")

        schedule_data_lst = list(set(schedule_data_lst))
        schedule_data_lst = json.dumps(schedule_data_lst, ensure_ascii=False)
        curr_group = json.dumps(curr_group, ensure_ascii=False)
        context = {'data': data, 'sportsall':sports, 'membersall':members,
                   'sports_date':sports_date, 'schedule_data':schedule_data, 'curr_group':curr_group, 'schedule_data_lst':schedule_data_lst}
        return render(request, 'cal/my_schedule.html', context )
    except:
        schedule_data_lst = []
        schedule_data_lst = json.dumps(schedule_data_lst, ensure_ascii=False)
        curr_group = json.dumps(curr_group, ensure_ascii=False)
        context = {'data': data, 'sportsall':sports, 'membersall':members, 'sports_date':sports_date, 'schedule_data':schedule_data,
                   'curr_group':curr_group, 'schedule_data_lst':schedule_data_lst}
        return render(request, 'cal/my_schedule.html', context)

def group_recommend(request):
    curr_group = request.session['curr_group']

    return render(request, 'cal/group_recommend.html')

def invite(request):

    return render(request, 'cal/calendar.html')

def mycalendar(request):

    loc = '09230740'
    url = 'https://weather.naver.com/today/%s' % (loc)
    raw = requests.get(url)
    html = bs4.BeautifulSoup(raw.text, 'html.parser')
    target = html.find('ul', {'class': 'week_list'})
    day_datas = target.find_all('div', {'class': 'day_data'})
    weather_dic = {}
    sports_dic = {}
    indoor_sports = ['3', '4', '6']
    outdoor_sports = ['1', '2', '5']
    ## 그룹 종목 출력 ##
    sportsall = CustomUser.objects.get(id= request.user.id).sports
    sportsall = ast.literal_eval(sportsall)
    sports = json.dumps(sportsall, ensure_ascii=False)

    ## 날씨 크롤링 ##
    for day_data in day_datas:
        date_data = day_data.find('span', {'class': 'date'})
        print(date_data)
        weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
        print(weather_inner)
        for day_data in day_datas:
            date_data = day_data.find('span', {'class': 'date'})
            weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
            print(weather_inner)
            for weathers in weather_inner:
                timeslot = weathers.find('span', {'class': 'timeslot'})
                weather = weathers.find('i', {'class': 'ico'})

                if timeslot.text == '오전':
                    # weather_dic[date_data.text] = []
                    # weather_dic[date_data.text].append(weather.text)
                    weather_dic[date_data.text] = weather.text

                    if weather.text == '흐리고 비' or weather.text == '비 또는 눈' or weather.text == '눈 또는 비' or weather.text == '가끔 비 또는 눈' \
                            or weather.text == '한때 비 또는 눈' or weather.text == '가끔 눈 또는 비' or weather.text == '한때 눈 또는 비' or \
                            weather.text == '안개' or weather.text == '연무' or weather.text == '박무 (엷은 안개)' or weather.text == '빗방울' \
                            or weather.text == '눈날림' or weather.text == '낙뢰' or weather.text == '황사' or weather.text == '비' or weather.text == '눈':
                        sports_dic[date_data.text] = list(set(sportsall) & set(indoor_sports))
                    elif weather.text == weather.text == '맑음' or weather.text == '구름많음' or weather.text == '구름조금' or weather.text == '흐림':
                        sports_dic[date_data.text] = list(set(sportsall) & set(outdoor_sports))

            #     json.dump(weather_dic, outfile, ensure_ascii=False)
        data = json.dumps(weather_dic, ensure_ascii=False)
        sports_date = json.dumps(sports_dic, ensure_ascii=False)

        print(sports)
        print(data)
        print(sports_date)
        context = {'data': data, 'sportsall': sports, 'sports_date': sports_date}
        return render(request, 'cal/mycalendar.html', context)
