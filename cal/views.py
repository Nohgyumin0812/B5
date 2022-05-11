
from django.shortcuts import render, get_object_or_404, redirect
from .form import MemberForm, SignupForm

def login(request):
    form = MemberForm()
    return render(request, 'login.html', {'form':form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = SignupForm()
    return render(request, 'signup.html', {'form':form})

def main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        member = Member.objects.get(username=username, password=password)
        if member is not None:
            request.session['memberId'] = member.id
            return render(request, 'main.html', {'memberId': member.name})
        else:
            return redirect('login')
        return render(request, 'main.html')