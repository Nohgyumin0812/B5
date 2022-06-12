from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import CustomUser
from cal.models import CustomGroup

#로그인 뷰함수
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'common/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'common/login.html')

#로그아웃 뷰함수
def logout(request):
    auth.logout(request)
    return redirect('/')

#회원가입 뷰함수
def signup(request):
    if request.method =='POST':
        print(request.POST)
        username=request.POST["username"]
        print(username)
        password=request.POST["password1"]

        email=request.POST["email"]
        tel = request.POST['tel']
        location = request.POST['location']
        if location == '이문동':
            location_code = '09230110'
            x= '127.062465'
            y= '37.598851'
        elif location == '회기동':
            location_code = '09230108'
            x= '127.051971'
            y= '37.591447'
        elif location == '휘경동':
            location_code = '09230108'
            x= '127.061228'
            y= '37.589592'
        elif location == '청량리동':
            location_code = '09230108'
            x= '127.044621'
            y= '37.586643'
        elif location == '전농동':
            location_code = '09230108'
            x= '127.053848'
            y= '37.579797'
        elif location == '제기동':
            location_code = '09230108'
            x= '127.03796'
            y= '37.584134'
        elif location == '용두동':
            location_code = '09230108'
            x= '127.034621'
            y= '37.576328'
        elif location == '신설동':
            location_code = '09230108'
            x= '127.026023'
            y= '37.575204'
        elif location == '답십리동':
            location_code = '09230108'
            x= '127.056757'
            y= '37.569883'
        elif location == '장안동':
            location_code = '09230108'
            x= '37.570749'
            y= '127.068233'

        sports = request.POST.getlist('sports[]')

        user= CustomUser.objects.create_user(username,email, password, tel = tel,location = location, sports = sports, location_code = location_code, x=x, y=y)
        user.save()

        return redirect('index')

    return render(request, 'common/signup.html')
