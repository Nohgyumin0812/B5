from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

####크롤링####
import requests
import bs4
import datetime as dt
############


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()


	def formatday(self, day, events):
		events_per_day = events.filter(date__day=day)

		"""
		loc = '09230740'
		url = 'https://weather.naver.com/today/%s' % (loc)
		raw = requests.get(url)
		html = bs4.BeautifulSoup(raw.text, 'html.parser')
		target = html.find('ul', {'class': 'week_list'})
		day_datas = target.find_all('div', {'class': 'day_data'})
		weather_lst = []

		for day_data in day_datas:
			date_data = day_data.find('span', {'class': 'date'})
			weather_inner = day_data.find_all('span', {'class': 'weather_inner'})
			for weathers in weather_inner:
				timeslot = weathers.find('span', {'class': 'timeslot'})
				weather = weathers.find('i', {'class': 'ico'})
				if timeslot.text == '오전':
					weather_lst.append([date_data.text, timeslot.text, weather.text])

		if day < dt.datetime.now().day:
			d = ''

		elif day <int(dt.datetime.now().day) + 1:
			d= weather_lst[0][2]

		elif day <int(dt.datetime.now().day) + 2:
			d= weather_lst[1][2]

		elif day <int(dt.datetime.now().day) + 3:
			d= weather_lst[2][2]

		elif day <int(dt.datetime.now().day) + 4:
			d= weather_lst[3][2]

		elif day <int(dt.datetime.now().day) + 5:
			d= weather_lst[4][2]

		elif day <int(dt.datetime.now().day) + 6:
			d= weather_lst[5][2]

		elif day <int(dt.datetime.now().day) + 7:
			d= weather_lst[6][2]

		elif day <int(dt.datetime.now().day) + 8:
			d= weather_lst[7][2]

		elif day <int(dt.datetime.now().day) + 9:
			d= weather_lst[8][2]

		elif day <int(dt.datetime.now().day) + 10:
			d= weather_lst[9][2]

		else:
			d = ''
	"""
		d=''
		print()
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
