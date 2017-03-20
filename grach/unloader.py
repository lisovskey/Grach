# -*- coding: utf-8 -*-

'''
парсим жопу
'''

from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup

def get_schedule(group, delta):
    '''
    получаем шедуле в лицо
    '''
    schedule = ''

    date = ''
    tmp_date = datetime.today() + timedelta(days=delta, hours=3)
    tmp_date = tmp_date.timetuple()
    date += str(tmp_date[2]) + '.' + str(tmp_date[1]) + '.' + str(tmp_date[0])

    tmp_week = requests.get('https://www.bsuir.by/schedule/rest/currentWeek/date/' + date)
    week_num = str(tmp_week.content)[2]
    if tmp_date[6] == 0:
        week_day = 'Понедельник'
        tmp_week = ' в понедельник'
    elif tmp_date[6] == 1:
        week_day = 'Вторник'
        tmp_week = ' во вторник'
    elif tmp_date[6] == 2:
        week_day = 'Среда'
        tmp_week = ' в среду'
    elif tmp_date[6] == 3:
        week_day = 'Четверг'
        tmp_week = ' в четверг'
    elif tmp_date[6] == 4:
        week_day = 'Пятница'
        tmp_week = ' в пятницу'
    elif tmp_date[6] == 5:
        week_day = 'Суббота'
        tmp_week = ' в субботу'
    elif tmp_date[6] == 6:
        week_day = 'Воскресенье'
        tmp_week = ' в воскресенье'
    schedule += tmp_week + ':'

    resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/' + str(group))
    soup = BeautifulSoup(resp.content, 'xml')
    day = soup.find_all('weekDay', text=week_day)
    if not day:
        return ' отдыхает'

    day = day[0].findParent('scheduleModel')
    subs = day.find_all('weekNumber', text=week_num)
    if not subs:
        return ' отдыхает'

    for subject in subs:
        schedule += '\n\n'
        subject = subject.find_parent('schedule')
        schedule += (subject.lessonTime.text + '\n' +
                     subject.subject.text + ' (' +
                     subject.lessonType.text + ') ')
        if subject.auditory is not None:
            schedule += subject.auditory.text
        if subject.numSubgroup.text != '0':
            schedule += ' (' + subject.numSubgroup.text + ')'
        if subject.lastName is not None and subject.numSubgroup.text == '0':
            schedule += ' ' + subject.lastName.text

    return schedule


def get_films(delta):
    '''
    получаем премьеры в лицо
    '''
    premieres = ''
    num = 1

    date = datetime.now() + timedelta(days=delta, hours=3)
    date = date.strftime('%d.%m.%Y')
    resp = requests.get('http://afisha.360.by/category-films_schedule.html')
    soup = BeautifulSoup(resp.content, 'html.parser')

    sub_soup = soup.body.section.select('.items-block > .items-sub-block > .cinema_slider > ul')[0]
    films = sub_soup.find_all('li', class_='scene')

    for film in films:
        film_title = film.select('.movie > .info > header > h1')[0]
        premieres += str(num) + '. ' + film_title.string + '\n'
        num += 1
    print(time.process_time())
    return premieres
