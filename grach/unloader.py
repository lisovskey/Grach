# -*- coding: utf-8 -*-

'''
parsers
'''

from datetime import datetime, timedelta
from requests import get
from urllib.request import urlopen
from requests.exceptions import ConnectionError
import bs4
import json


def get_schedule(group, delta):
    '''
    return schedule from bsuir.by with delta days
    '''
    schedule = ''
    try:
        full_schedule = json.load(
            urlopen('http://students.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group))
    except(ConnectionError):
        return None

    tmp_date = datetime.today() + timedelta(days=delta, hours=3)
    tmp_date = tmp_date.timetuple()

    day_num = tmp_date[6]
    week_num = full_schedule['currentWeekNumber']
    if datetime.today().weekday() == 5 or datetime.today().weekday() == 6:
        if week_num == 4:
            week_num = 1
        else:
            week_num += 1

    if day_num == 0:
        week_day = 'Понедельник'
        tmp_week = ' в понедельник'
    elif day_num == 1:
        week_day = 'Вторник'
        tmp_week = ' во вторник'
    elif day_num == 2:
        week_day = 'Среда'
        tmp_week = ' в среду'
    elif day_num == 3:
        week_day = 'Четверг'
        tmp_week = ' в четверг'
    elif day_num == 4:
        week_day = 'Пятница'
        tmp_week = ' в пятницу'
    elif day_num == 5:
        week_day = 'Суббота'
        tmp_week = ' в субботу'
    elif day_num == 6:
        week_day = 'Воскресенье'
        tmp_week = ' в воскресенье'
    schedule += tmp_week + ':'

    try:
        subject = full_schedule['schedules'][day_num]
    except IndexError:
        return ' отдыхает'

    if delta == 0:
        subs = full_schedule['todaySchedules']
    elif delta == 1:
        subs = full_schedule['tomorrowSchedules']
    else:
        subs = full_schedule['schedules'][day_num]['schedule']
    for subject in subs:
        if week_num in subject['weekNumber']:
            schedule += '\n\n' + subject['lessonTime'] + '\n' + \
                        subject['subject'] + ' (' + \
                        subject['lessonType'] + ') '
            if subject['auditory']:
                schedule += subject['auditory'][0]
            if subject['numSubgroup'] != 0:
                schedule += ' (' + str(subject['numSubgroup']) + ')'
            if subject['employee'] and subject['numSubgroup'] == 0:
                schedule += ' ' + subject['employee'][0]['lastName']

    return schedule


def get_films(delta):
    '''
    return list of films from 360.by
    '''
    premieres = ''

    date = datetime.now() + timedelta(days=delta, hours=3)
    date = date.strftime('%d.%m.%Y')
    try:
        resp = get('https://afisha.360.by/category-films_schedule.html')
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    except (ConnectionError, bs4.FeatureNotFound):
        return None

    sub_soup = soup.body.section.select('.items-block > .items-sub-block > .cinema_slider > ul')[0]
    films = sub_soup.find_all('li', class_='scene')

    for i, film in enumerate(films):
        film_title = film.select('.movie > .info > header > h1')[0]
        premieres += str(i + 1) + '. ' + film_title.string + '\n'

    return premieres


def get_cryptorate(currency_name):
    '''
    return exchange rate if exists
    '''
    try:
        currency = get('https://api.coinmarketcap.com/v1/ticker/' + currency_name).json()[0]
        rate = currency['price_usd']
    except KeyError:
        rate = None

    return rate
