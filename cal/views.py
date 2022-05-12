<<<<<<< HEAD

from django.shortcuts import render, get_object_or_404, redirect
from .form import MemberForm, SignupForm

<<<<<<< HEAD
from .models import *
from .utils import Calendar
from .forms import EventForm

def index(request):
    return render(request, 'cal/main.html')


def signup(request):
    """
    회원가입
    """
    form =""
    return render(request, 'cal/signup.html', {'form':form})

def calendar(request):
    return render(request, 'cal/calendar.html')

def group_making(request):
    return render(request, 'cal/group_making.html')

def group_managing(request):
    return render(request, 'cal/group_managing.html')





"""
class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

##일정저장 및 수정##
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and 'save' in request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))

##일정삭제##
    if request.POST and 'delete' in request.POST:
        if event_id:
            Event.objects.filter(pk=event_id).delete()
            return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})
"""
=======
=======

from django.shortcuts import render, get_object_or_404, redirect
from .form import MemberForm, SignupForm

>>>>>>> fede2d955a2c0055c41e2159225127809f9607dd
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
<<<<<<< HEAD
        return render(request, 'main.html')
>>>>>>> fede2d955a2c0055c41e2159225127809f9607dd
=======
        return render(request, 'main.html')
>>>>>>> fede2d955a2c0055c41e2159225127809f9607dd
