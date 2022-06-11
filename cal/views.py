import json
from urllib import parse
from urllib.parse import unquote, quote, quote_plus, urlencode
import bs4
import requests
from django.contrib.auth.decorators import login_required
import json
import calendar
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import ast
from .forms import GroupForm, DayForm, InviteForm, InviteGroupForm, ScheForm, my_ScheForm
from .models import CustomGroup, DayGroup, InviteGroup,InviteGroupGroup, ScheGroup, my_ScheGroup
from common.models import CustomUser
from .models import Event

from django.contrib.auth.models import Group
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import urllib

def index(request):
    return render(request, 'common/login.html')

@login_required()
def calendar(request):
    curr_url = parse.unquote(str(request.build_absolute_uri()))
    curr_url = curr_url.split('/')

    if curr_url[4] == '':
        return render(request, 'cal/mycalendar.html')

    curr_group = (curr_url[4]).replace('?', '')
    curr_group_id = CustomGroup.objects.filter(groupname = curr_group).values()[0]['id']
    ##함께하기 방장만 가능##
    my_id = CustomUser.objects.filter(id=request.user.id).values()[0]['id']
    owner_id = CustomGroup.objects.filter(groupname = curr_group).values()[0]['owner_id']

    my_name = CustomUser.objects.filter(id=request.user.id).values()[0]['username']
    owner_name = CustomUser.objects.filter(id = owner_id).values()[0]['username']

    my_name = json.dumps(my_name,ensure_ascii=False )
    owner_name = json.dumps(owner_name,ensure_ascii=False )
    print(my_name)
    print(owner_name)

    if request.method == "POST":
        if my_id == owner_id:
            if 'invite-name' in request.POST:
                form = InviteForm(request.POST)
                if form.is_valid():
                    Invite = form.save(commit=False)
                    new_member = str(request.POST['invite-name']).replace("'", '')
                    print(new_member)
                    Invite.invite_user = new_member
                    Invite.group = curr_group
                    Invite.invite_status = 1
                    Invite = form.save()
                    print("#####################")

            if "sche-name" in request.POST:
                print(request.POST)
                form = ScheForm(request.POST)
                if form.is_valid():
                    Sche = form.save(commit = False)
                    Sche.sche_name = request.POST['sche-name']
                    Sche.sche_date = request.POST['sche-date']
                    Sche.sche_memo = request.POST['sche-memo']
                    Sche.group_id = curr_group_id
                Sche = form.save()
                print("######")

        ##강퇴기능은 값 받아와야 함, 리스트에서 값 받아오면 수정
            if "kickList[]" in request.POST:
                #멤버 삭제
                print("@@@@@@@@@@@@")
                print(request.POST)
                item = CustomGroup.objects.get(groupname=curr_group)
                kickOut_member = request.POST['kickList[]']
                new_friendname = ast.literal_eval(item.friendname)
                new_friendname.remove(kickOut_member)
                item.friendname = new_friendname
                item.save()
                #가능 날짜 삭제
                kickOut_member_id = CustomUser.objects.filter(username = kickOut_member).values()[0]['id']
                item_Day = DayGroup.objects.filter(group_id = curr_group_id,user_id = kickOut_member_id )
                item_Day.delete()
                for item_day in item_Day:
                    item_day.save()
    ## 일정 추가 ##
    try:
        sche_data = ScheGroup.objects.filter(group_id = curr_group_id).values()
        sche_data = pd.DataFrame(sche_data).drop(['id', 'group_id'], axis = 1).set_index('sche_date').T.to_dict('list')
        print(sche_data)
    except:
        sche_data = ""

    sche_data = json.dumps(sche_data, ensure_ascii= False)
    loc = CustomGroup.objects.filter(groupname = curr_group).values()[0]['location_code']
    url = 'https://weather.naver.com/today/%s' % (loc)
    raw = requests.get(url)
    html = bs4.BeautifulSoup(raw.text, 'html.parser')
    target = html.find('ul', {'class': 'week_list'})
    day_datas = target.find_all('div', {'class': 'day_data'})
    weather_dic = {}
    sports_dic = {}
    indoor_sports = ['3', '4', '6']
    outdoor_sports = ['1', '2', '5']

    try:
        ## 그룹 종목 출력 ##
        sportsall = CustomGroup.objects.get(groupname=curr_group).sports
        sportsall = ast.literal_eval(sportsall)
        sports = json.dumps(sportsall, ensure_ascii=False)

        ## 날씨 크롤링 ##
        for day_data in day_datas:
            date_data = day_data.find('span', {'class': 'date'})
            weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
            for weathers in weather_inner:
                timeslot = weathers.find('span', {'class': 'timeslot'})
                weather = weathers.find('i', {'class': 'ico'})

                if timeslot.text == '오전':
                    #weather_dic[date_data.text] = []
                    # weather_dic[date_data.text].append(weather.text)
                    weather_dic[date_data.text] = weather.text
                    if '비' in weather.text or weather.text == '흐리고 비' or weather.text == '흐리고 한때 비' or weather.text == '흐리고 가끔 비' or weather.text == '비 또는 눈' or weather.text ==  '눈 또는 비' or weather.text == '가끔 비 또는 눈' \
                            or weather.text == '한때 비 또는 눈' or weather.text == '가끔 눈 또는 비' or weather.text == '한때 눈 또는 비' or \
                            weather.text == '안개' or weather.text == '연무' or weather.text == '박무 (엷은 안개)' or weather.text == '빗방울' \
                            or weather.text == '눈날림' or weather.text == '낙뢰' or weather.text == '황사' or weather.text == '비' or weather.text == '눈':
                        sports_dic[date_data.text] = list(set(sportsall) & set(indoor_sports))
                    elif weather.text == weather.text == '맑음' or weather.text == '구름많음' or weather.text == '구름조금' or weather.text == '흐림':
                        sports_dic[date_data.text] = list(set(sportsall) & set(outdoor_sports))
                    else:
                        sports_dic[date_data.text] = "날씨없음"

    # file_path = "./sample.json"
    # with open(file_path, 'w') as outfile:
    #     json.dump(weather_dic, outfile, ensure_ascii=False)

        if len(weather_dic) == 11:
            weather_dic.popitem()
            sports_dic.popitem()

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


        ##날짜 출력##
        try:
            my_id = CustomUser.objects.get(id=request.user.id).username
            schedule_data = DayGroup.objects.filter(group_id=my_group_id).values_list()
            print("##############")
            schedule_data = pd.DataFrame(schedule_data)

            schedule_data.columns = ["id", "group_id", "myDates", "username"]
            for i in range(schedule_data.shape[0]):
                schedule_data.iloc[:, 3][i] = CustomUser.objects.get(id = str(schedule_data.iloc[:, 3][i]))
                schedule_data.iloc[:,3][i] = str(schedule_data.iloc[:, 3][i])
                schedule_data['myDates'][i] = ast.literal_eval(str([schedule_data['myDates'][i]]).replace(' ',''))

            schedule_data_lst = schedule_data.iloc[:, 2:].groupby('username').sum()


            for i in range(schedule_data_lst.shape[0]):
                schedule_data_lst['myDates'][i] = str(schedule_data_lst['myDates'][i]).replace(' ','').replace("','", ",").replace(',', "','")
                schedule_data_lst['myDates'][i] = ast.literal_eval(schedule_data_lst['myDates'][i])
                schedule_data_lst['myDates'][i] = list(set(schedule_data_lst['myDates'][i]))
            for i in range(schedule_data_lst['myDates'].shape[0]):
                for j in range(len(schedule_data_lst['myDates'][i])):
                    if len(str(schedule_data_lst['myDates'][i][j])) ==3:
                        schedule_data_lst['myDates'][i][j] = str(schedule_data_lst['myDates'][i][j])[:1] + ".0" + str(schedule_data_lst['myDates'][i][j])[-1] + "."
                    else:
                        schedule_data_lst['myDates'][i][j] = str(schedule_data_lst['myDates'][i][j]) + "."
            schedule_data_dic_2 = pd.DataFrame(schedule_data_lst['myDates']).to_dict()['myDates']
            schedule_data_dic = json.dumps(schedule_data_dic_2, ensure_ascii= False)
            print(schedule_data_dic)
            ## 일정 추천 ##
            schedule_data_dic_2 = pd.DataFrame(schedule_data_dic_2.items(), columns=['name', 'date'])
            for i in range(schedule_data_dic_2.shape[0]):
                schedule_data_dic_2['date'][i] = str(schedule_data_dic_2['date'][i]).replace('[', '').replace(']',
                                                                                                              '').replace(
                    "'", '').replace(' ', '')

            schedule_data_dic_2 = pd.concat([pd.Series(row['name'], row['date'].split(','))
                                             for _, row in schedule_data_dic_2.iterrows()]).reset_index()

            schedule_data_dic_2.iloc[:, 1] = 1
            schedule_data_dic_2 = schedule_data_dic_2.groupby('index').sum().reset_index()
            schedule_data_dic_2.columns = ['date', 'member']
            sports_df = pd.DataFrame(sports_dic.items(), columns=['date', 'sports'])
            for i in range(sports_df.shape[0]):
                sports_df['sports'][i] = len(sports_df['sports'][i])

            df_recommend = pd.merge(sports_df, schedule_data_dic_2, left_on='date', right_on='date', how='inner')

            sports_percent = int(CustomGroup.objects.filter(groupname = curr_group).values()[0]['dateFirst'])

            member_percent = int(CustomGroup.objects.filter(groupname = curr_group).values()[0]['sportFirst'])

            print(sports_percent)
            print(member_percent)
            df_recommend['point'] = sports_percent * df_recommend['sports'] + member_percent * df_recommend['member']
            df_recommend['rank_point'] = df_recommend['point'].rank(method='min')
            rank_point = list(set(list(df_recommend['rank_point'])))
            rank_point.sort(reverse=True)
            print(rank_point)

            for i in range(df_recommend['rank_point'].shape[0]):
                if df_recommend['rank_point'][i] == rank_point[0]:
                    df_recommend['rank_point'][i] = '완전추천'
                elif df_recommend['rank_point'][i] == rank_point[1]:
                    df_recommend['rank_point'][i] = '추천'
                else:
                    df_recommend['rank_point'][i] = ''

            recommend = df_recommend[['date', 'rank_point']].to_dict('records')
            recommend = json.dumps(recommend, ensure_ascii=False)
            print(recommend)

        except:
            schedule_data_dic = []
            recommend = []

        context = {'data': data, 'sportsall':sports, 'membersall':members,
                   'sports_date':sports_date, 'schedule_data_dic':schedule_data_dic,
                   'my_name':my_name, 'owner_name':owner_name, 'recommend':recommend, 'sche_data':sche_data}

        return render(request, 'cal/calendar.html', context)
    except CustomGroup.DoesNotExist:
        return render(request, 'cal/group_making.html')

@login_required()
def group_making(request):
    if request.method == 'POST':
        print(request.POST)

        form = GroupForm(request.POST)
        print(form)
        if form.is_valid():
            group = form.save(commit=False)
            print('##################')
            group.owner = request.user
            group.group_name = request.POST["groupname"]
            group.sports = request.POST.getlist('sports')
            group.friendname = request.POST.getlist("friendname")
            group.invite_status = 0
            print(group.friendname)

            group.location = request.POST['g-location']
            if group.location == '이문동':
                group.location_code = '09230110'
                group.x = '127.062465'
                group.y = '37.598851'
            elif group.location == '회기동':
                group.location_code = '09230108'
                group.x = '127.051971'
                group.y = '37.591447'
            elif group.location == '휘경동':
                group.location_code = '09230108'
                group.x = '127.061228'
                group.y = '37.589592'
            elif group.location == '청량리동':
                group.location_code = '09230108'
                group.x = '127.044621'
                group.y = '37.586643'
            elif group.location == '전농동':
                group.location_code = '09230108'
                group.x = '127.053848'
                group.y = '37.579797'
            elif group.location == '제기동':
                group.location_code = '09230108'
                group.x = '127.03796'
                group.y = '37.584134'
            elif group.location == '용두동':
                group.location_code = '09230108'
                group.x = '127.034621'
                group.y = '37.576328'
            elif group.location == '신설동':
                group.location_code = '09230108'
                group.x = '127.026023'
                group.y = '37.575204'
            elif group.location == '답십리동':
                group.location_code = '09230108'
                group.x = '127.056757'
                group.y = '37.569883'
            elif group.location == '장안동':
                group.location_code = '09230108'
                group.x = '37.570749'
                group.y = '127.068233'

            group.dateFirst = request.POST['dateFirst']
            group.sportFirst = request.POST['sportFirst']

            group.save()
            return redirect('cal:group_managing')
    return render(request, 'cal/group_making.html')

#2015
#00016

@csrf_exempt
@login_required()
def group_managing(request):
    my_group = []
    group = CustomGroup.objects.all().values()
    user = CustomUser.objects.all().values()
    username = CustomUser.objects.get(id=request.user.id).username
    df = pd.DataFrame(group)
    df_user = pd.DataFrame(user)

    try:
        ##그룹 요청-개인##
        courses = InviteGroup.objects.filter(invite_user=request.user.username, invite_status=1).values()
        courses = pd.DataFrame(courses)

        courses['num_member'] = 0
        courses['sports'] = "22"
        for i in range(courses.shape[0]):
            courses['num_member'][i] = len(ast.literal_eval(str(CustomGroup.objects.filter
                                                                (groupname=courses['group'][i]).values()[0][
                                                                    'friendname']).replace(' ', ''))) + 1
            courses['sports'] = CustomGroup.objects.filter(groupname=courses['group'][i]).values()[0]['sports']
        courses = courses[['group', 'num_member', 'sports']].set_index('group').T.to_dict()

        invite_member_dic = {}
        invite_member_dic['개인초대'] = courses
        print(invite_member_dic)
    except:
        invite_member_dic = {}


        ## 그룹요청-그룹##
    courses_group = InviteGroupGroup.objects.filter(owner_id = request.user.id, invite_status = 1).values()
    courses_group = pd.DataFrame(courses_group)

    #courses_group = InviteGroupGroup.objects.filter()
    print(1)

    invite_group = json.dumps(invite_member_dic, ensure_ascii=False)


    ##그룹 관리##
    try:
        df_inner_join = []
        df_group = (pd.DataFrame(df[['groupname','owner_id', 'friendname']]))
        df_user['owner_id']= df_user['id']
        df_user = (df_user[['owner_id', 'username']])
        df_inner_join = pd.merge(df_group, df_user, left_on = 'owner_id', right_on = 'owner_id', how = 'inner')
        #print(df_user[df_user['id'] == df['owner_id']])
        df_inner_join['member_num'] = 0
        df_inner_join['sports'] = ""
        df_inner_join['true'] = 0

        for i in range(df_inner_join.shape[0]):
            df_inner_join['username'][i] = [df_inner_join['username'][i]]
            df_inner_join['friendname'][i] = ast.literal_eval(df_inner_join['friendname'][i])+(df_inner_join['username'][i])
            df_inner_join['member_num'][i] = len(df_inner_join['friendname'][i])
            df_inner_join['sports'][i] = CustomGroup.objects.filter(groupname = df_inner_join['groupname'][i]).values()[0]['sports']
            if username in df_inner_join['friendname'][i]:
                df_inner_join['true'][i] = 1
                my_group.append(df_inner_join['groupname'][i])
        #pd.set_option('display.max_columns', None)
        group_json = json.dumps(my_group, ensure_ascii=False)
        df_inner_join = df_inner_join[df_inner_join['true'] ==1]

        df_inner_join = df_inner_join[['groupname', 'member_num', 'sports']]
        df_inner_join = df_inner_join.set_index('groupname').T.to_dict()
        df_inner_join = json.dumps(df_inner_join, ensure_ascii= False)        ## 내 그룹 시 그룹명, 멤버수, 종목 출력 ##

        if request.method == "POST":
            invite_group_name = request.POST.get('g_name')
            print(request.POST)
            Invite_item = InviteGroup.objects.get(group=invite_group_name, invite_user=username, invite_status=1)
            Invite_item.invite_status = 0
            Invite_item.save()
            group_item = CustomGroup.objects.get(groupname=invite_group_name)
            if CustomGroup.objects.filter(groupname=invite_group_name).values()[0]['friendname'] == "[]":
                group_item.friendname = "['" + str(username) + "']"
            elif len(ast.literal_eval(CustomGroup.objects.filter(groupname=invite_group_name).values()[0]['friendname'])) == 1:
                group_item.friendname = "[" + str(group_item.friendname).replace("[", '').replace(']', '') + ",'" + str(username) + "']"
            else:
                group_item.friendname = "[" + str(group_item.friendname).replace("[", '').replace(']', '') + ",'" + str(username) + "']"

            group_item.friendname = ast.literal_eval(group_item.friendname)
            group_item.save()
            return redirect('cal:group_managing')
        return render(request, 'cal/group_managing.html', {'my_group':my_group, 'invite_group':invite_group, 'df_inner_join':df_inner_join})
    except:
        return render(request, 'cal/group_managing.html', {'my_group':my_group, 'invite_group':invite_group, 'df_inner_join':df_inner_join})


def my_schedule(request):
    schedule_data = []
    data = request.session['data']
    sports = request.session['sports']
    members = request.session['members']
    sports_date = request.session['sports_date']
    curr_group = request.session['curr_group']
    my_group_id = CustomGroup.objects.get(groupname = curr_group ).id

    #my_schedule 데이터 전송 확인 부분
    if request.method == 'POST':
        schedule_data = request.POST["myDates"]

        form = DayForm(request.POST)
        if form.is_valid():
            Day = form.save(commit=False)
            Day.group_id = CustomGroup.objects.get(groupname = curr_group ).id
            Day.dates = str(schedule_data)
            Day.user_id = request.user.id
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
                   'sports_date':sports_date, 'curr_group':curr_group}
        return render(request, 'cal/my_schedule.html', context )
    except:
        schedule_data_lst = []
        schedule_data_lst = json.dumps(schedule_data_lst, ensure_ascii=False)
        curr_group = json.dumps(curr_group, ensure_ascii=False)
        context = {'data': data, 'sportsall':sports, 'membersall':members,
                   'sports_date':sports_date,'curr_group':curr_group}
        return render(request, 'cal/my_schedule.html', context)

def group_recommend(request):
    ##내 주변 그룹##
    curr_group = request.session['curr_group']
    group_x = CustomGroup.objects.filter(groupname=curr_group).values()[0]['x']
    group_y = CustomGroup.objects.filter(groupname=curr_group).values()[0]['y']

    df_group = pd.DataFrame(CustomGroup.objects.all().values())

    indexNames = df_group[df_group['groupname']==curr_group].index
    df_group.drop(indexNames, inplace = True)
    df_group = df_group[df_group['invite_status'] == '0']
    df_group['x'] = df_group['x'].astype(float)
    df_group['y'] = df_group['y'].astype(float)
    df_group['distance'] = (df_group['x'] - float(group_x))**2 + (df_group['y']- float(group_y))**2

    df_group = df_group.sort_values(by = 'distance', ascending= True)
    place_group = df_group[['location', 'groupname']].to_dict('records')

    ##상대팀이 될 수 있는 그룹##
    group_sports = ast.literal_eval(CustomGroup.objects.filter(groupname=curr_group).values()[0]['sports'])
    sports_group = df_group[['groupname', 'sports']]

    sports_group = sports_group.reset_index(drop = True)
    sports_group['common'] = 0
    for i in range(sports_group.shape[0]):
        sports_group['common'][i] = len(set(ast.literal_eval(sports_group['sports'][i])) & set(group_sports))
    sports_group = sports_group.sort_values(by = 'common', ascending = False)
    sports_group = sports_group.to_dict('records')

    if request.method == "POST":
        form = InviteGroupForm(request.POST)
        if form.is_valid():
            InviteGroup = form.save(commit=False)
            new_group = str(request.POST['rg_name']).replace("'", '')
            print(request.POST)
            InviteGroup.invite_group = new_group
            InviteGroup.group = curr_group
            owner_id = CustomGroup.objects.filter(groupname= new_group).values()[0]['owner_id']
            InviteGroup.invite_status = '1'
            InviteGroup.owner_id = owner_id
            InviteGroup = form.save()
        return redirect('cal:group_recommend')

    ##초대상태##
    place_group = pd.DataFrame(place_group)  # distance: 내 그룹과 상대 그룹 간의 거리
    sports_group = pd.DataFrame(sports_group)
    invite_length = len(InviteGroupGroup.objects.filter(group = curr_group, invite_status = 1).values())
    invite_loc_list = []
    invite_spo_list = []
    for i in range(invite_length):
        invite_loc_list.append(InviteGroupGroup.objects.filter(group = curr_group, invite_status = 1).values()[i]['invite_group'])
        invite_spo_list.append(InviteGroupGroup.objects.filter(group = curr_group, invite_status = 1).values()[i]['invite_group'])

    place_group = place_group[~place_group['groupname'].isin(invite_loc_list)]
    place_group = place_group[['location', 'groupname']].to_dict('records')

    sports_group = sports_group[~sports_group['groupname'].isin(invite_spo_list)]
    sports_group = sports_group[['sports', 'groupname']].to_dict('records')

    ##스포츠그룹-초대상태##
    print(sports_group) # common: 겹치는 운동종목 수

    place_group = json.dumps(place_group, ensure_ascii=False)
    sports_group = json.dumps(sports_group, ensure_ascii=False)

    context = {'place_group': place_group,'sports_group':sports_group}
    return render(request, 'cal/group_recommend.html', context)

def mycalendar(request):
    loc = CustomUser.objects.filter(id= request.user.id).values()[0]['location_code']
    url = 'https://weather.naver.com/today/%s' % (loc)
    raw = requests.get(url)
    html = bs4.BeautifulSoup(raw.text, 'html.parser')
    target = html.find('ul', {'class': 'week_list'})
    day_datas = target.find_all('div', {'class': 'day_data'})
    weather_dic = {}
    sports_dic = {}
    indoor_sports = ['3', '4', '6']
    outdoor_sports = ['1', '2', '5']

    if request.method == 'POST':
        if "sche-name" in request.POST:
            print(request.POST)
            form = my_ScheForm(request.POST)
            if form.is_valid():
                Sche = form.save(commit=False)
                Sche.sche_name = request.POST['sche-name']
                Sche.sche_date = request.POST['sche-date']
                Sche.sche_memo = request.POST['sche-memo']
                Sche.user_id = request.user.id
            Sche = form.save()
            print("######")

    ##개인 일정 추가##
    try:
        sche_data = my_ScheGroup.objects.filter(id = request.user.id).values()
        sche_data = pd.DataFrame(sche_data).drop(['id', 'user_id'], axis = 1).set_index('my_sche_date').T.to_dict('list')
        sche_data = json.dumps(sche_data, ensure_ascii= False)
        print(sche_data)
    except:
        sche_data = ""
    sche_data = json.dumps(sche_data, ensure_ascii= False)
    ## 그룹 종목 출력 ##
    sportsall = CustomUser.objects.get(id= request.user.id).sports
    sportsall = ast.literal_eval(sportsall)
    sports = json.dumps(sportsall, ensure_ascii=False)

    ## 날씨 크롤링 ##
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
                if '비' in weather.text or weather.text == '흐리고 비' or weather.text == '흐리고 한때 비' or weather.text == '흐리고 가끔 비' or weather.text == '비 또는 눈' or weather.text == '눈 또는 비' or weather.text == '가끔 비 또는 눈' \
                        or weather.text == '한때 비 또는 눈' or weather.text == '가끔 눈 또는 비' or weather.text == '한때 눈 또는 비' or \
                        weather.text == '안개' or weather.text == '연무' or weather.text == '박무 (엷은 안개)' or weather.text == '빗방울' \
                        or weather.text == '눈날림' or weather.text == '낙뢰' or weather.text == '황사' or weather.text == '비' or weather.text == '눈':
                    sports_dic[date_data.text] = list(set(sportsall) & set(indoor_sports))
                elif weather.text == weather.text == '맑음' or weather.text == '구름많음' or weather.text == '구름조금' or weather.text == '흐림':
                    sports_dic[date_data.text] = list(set(sportsall) & set(outdoor_sports))
                else:
                    sports_dic[date_data.text] = "날씨없음"
            #     json.dump(weather_dic, outfile, ensure_ascii=False)
    if len(weather_dic) == 11:
        weather_dic.popitem()
        sports_dic.popitem()

    data = json.dumps(weather_dic, ensure_ascii=False)
    sports_date = json.dumps(sports_dic, ensure_ascii=False)
    context = {'data': data, 'sportsall': sports, 'sports_date': sports_date, 'sche_data':sche_data}
    return render(request, 'cal/mycalendar.html', context)
