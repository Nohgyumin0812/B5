from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import CustomUser
from cal.models import CustomGroup
#로그인 구현
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

#로그아웃 구현
def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method =='POST':
        username=request.POST["username"]
        print(username)
        print(request.POST)
        password=request.POST["password1"]
        email=request.POST["email"]
        tel = request.POST['tel']

        sports = request.POST.getlist('sports[]')

        user= CustomUser.objects.create_user(username,email, password, tel = tel, sports = sports)
        user.save()

        return redirect('index')

    return render(request, 'common/signup.html')
