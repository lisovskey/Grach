# -*- coding: utf-8 -*-

'''
парсим жопу
'''

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulStoneSoup as Soup

class Unloader:
    '''
    ну это типа парсер
    '''
    def __init__(self):
        '''
        создаем парсера
        '''
        pass


    def get_schedule(self, group, delta):
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
        pretext = 'в'
        if tmp_date[6] == 0:
            week_day = 'Понедельник'
            tmp_week = 'понедельник'
        elif tmp_date[6] == 1:
            week_day = 'Вторник'
            pretext = 'во'
            tmp_week = 'вторник'
        elif tmp_date[6] == 2:
            week_day = 'Среда'
            tmp_week = 'среду'
        elif tmp_date[6] == 3:
            week_day = 'Четверг'
            tmp_week = 'четверг'
        elif tmp_date[6] == 4:
            week_day = 'Пятница'
            tmp_week = 'пятницу'
        elif tmp_date[6] == 5:
            week_day = 'Суббота'
            tmp_week = 'субботу'
        elif tmp_date[6] == 6:
            week_day = 'Воскресенье'
            tmp_week = 'воскресенье'
        schedule += pretext + ' ' + tmp_week + ':'

        resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/' + str(group))
        soup = Soup(resp.content)
        day = soup.findAll('weekDay', text=week_day)
        if not day:
            return 'отдыхает'

        day = day[0].findParent('scheduleModel')
        subs = day.findAll('weekNumber', text=week_num)
        if not subs:
            return 'отдыхает'

        for subject in subs:
            schedule += '\n\n'
            subject = subject.findParent('schedule')
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


    def get_premieres(self):
        '''
        получаем премьеры в лицо
        '''
        premieres = ''

        return premieres
