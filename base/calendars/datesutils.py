'''
This are group of functions and utilities used to hlp with dates calculations

'''

import datetime
from datetime import timedelta, date
import calendar

def add_month(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)
	
def add_months(start_date, end_date, number_of_months):
	dates = []
	cur_date= start_date
	dates.append(cur_date)
	while cur_date< end_date:
		cur_date = add_month(cur_date, 1)
		print(cur_date)
		dates.append(cur_date)
	return dates
	
def add_days(start_date, end_date, interval):
	dates = []
	cur_date= start_date
	dates.append(cur_date)
	while cur_date< end_date:
		cur_date += datetime.timedelta(days=interval)
		dates.append(cur_date)
	return dates

def daterange(start_date, end_date, interval_type, interval):
	cur_date = start_date
	dates=[]
	dates.append(start_date)
	print (interval_type)
	if (interval_type == 'week'):
		interval = interval *7
		dates = add_days(start_date, end_date, interval)
	elif (interval_type == 'day'):
		dates = add_days(start_date, end_date, interval)
	elif interval_type == 'month':
		dates = add_months(start_date, end_date, interval)
	
	return dates


#this function gets the date for a first day i.e. if passed as next_weekday(date,0) returns first monday after the given date
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)