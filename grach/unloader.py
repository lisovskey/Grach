# -*- coding: utf-8 -*-

'''
parsers
'''

from datetime import datetime, timedelta
import json
from urllib.request import urlopen
from requests import get
from requests.exceptions import ConnectionError
import bs4


SHEDULE_URL = 'http://students.bsuir.by/api/v1/studentGroup/schedule?studentGroup='
FILMS_URL = 'http://afisha.360.by/category-films_schedule.html'
CRYPTORATE_URL = 'https://api.coinmarketcap.com/v1/ticker/'


def get_schedule(group, delta):
    '''
    return schedule from bsuir.by with delta days
    '''
    week_days = ['в понедельник', 'во вторник', 'в среду', 'в четверг',
                 'в пятницу', 'в субботу', 'в воскресенье']

    try:
        full_schedule = json.load(urlopen(SHEDULE_URL + group))
    except ConnectionError:
        return None

    request_date = datetime.today() + timedelta(days=delta)
    day_num = request_date.timetuple()[6]
    week_num = full_schedule['currentWeekNumber']
    if datetime.today().weekday() == 5 or datetime.today().weekday() == 6:
        if week_num == 4:
            week_num = 1
        else:
            week_num += 1

    schedule = '{} {}'.format(group, week_days[day_num])

    try:
        subject = full_schedule['schedules'][day_num]
        schedule += ':'
    except IndexError:
        return schedule + ' отдыхает'

    if delta == 0:
        subs = full_schedule['todaySchedules']
    elif delta == 1:
        subs = full_schedule['tomorrowSchedules']
    else:
        subs = full_schedule['schedules'][day_num]['schedule']

    for subject in subs:
        if week_num in subject['weekNumber']:
            schedule += '\n\n{}\n{} ({}) '.format(subject['lessonTime'],
                                                  subject['subject'],
                                                  subject['lessonType'])
            if subject['auditory']:
                schedule += subject['auditory'][0]
            if subject['numSubgroup'] != 0:
                schedule += ' ({})'.format(str(subject['numSubgroup']))
            if subject['employee'] and subject['numSubgroup'] == 0:
                schedule += ' {}'.format(subject['employee'][0]['lastName'])

    return schedule


def get_films(delta):
    '''
    return list of films from 360.by
    '''
    premieres = ''

    date = datetime.now() + timedelta(days=delta, hours=3)
    date = date.strftime('%d.%m.%Y')
    try:
        resp = get(FILMS_URL)
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    except (ConnectionError, bs4.FeatureNotFound):
        return None

    sub_soup = soup.body.section.select('.items-block > .items-sub-block > .cinema_slider > ul')[0]
    films = sub_soup.find_all('li', class_='scene')

    for i, film in enumerate(films):
        film_title = film.select('.movie > .info > header > h1')[0]
        premieres += '{}. {}\n'.format(str(i + 1), film_title.string)

    return premieres


def get_cryptorate(currency_name):
    '''
    return exchange rate if exists
    '''
    try:
        currency = get(CRYPTORATE_URL + currency_name).json()[0]
        return currency['price_usd']
    except KeyError:
        return None
