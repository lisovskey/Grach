# -*- coding: utf-8 -*-

'''
работаем
'''

from datetime import datetime, date, time, timedelta
import telebot
import requests
from bs4 import BeautifulStoneSoup as Soup

class RZTeleBot(telebot.TeleBot):
    '''
    ну это типа грач
    '''
    def __init__(self, token):
        '''
        создаем грача
        '''
        super().__init__(token)
        print(self.get_me())

    def log(self, received_message, answer):
        '''
        логируем в консоль
        '''
        print('----------------------------------------------------------------')
        print('{0} {1} (id {2})'.format(received_message.from_user.first_name,
                                        received_message.from_user.last_name,
                                        received_message.from_user.id), end='')
        if received_message.chat.id != received_message.from_user.id:
            print(' in {0} (id {1}): '.format(received_message.chat.title,
                                              received_message.chat.id))
        else:
            print(': ')
        print(' - {}'.format(received_message.text))
        print('Отвечаю: ')
        print(' - {}'.format(answer))

    def reply(self, received_message, send_what, to_chat_id, answer):
        '''
        посылаем с логом
        экспериментальная хуйня
        '''
        self.log(received_message, answer)
        send_what(to_chat_id, answer)

    def get_schedule(self, group, delta):
        '''
        schedule takes group and delta days and returns day's schedule
        '''
        schedule = ''

        date = ''
        tmp_date = datetime.today() + timedelta(days=delta, hours=3)
        print(tmp_date.time())
        tmp_date = tmp_date.timetuple()
        date += str(tmp_date[2]) + '.' + str(tmp_date[1]) + '.' + str(tmp_date[0])

        tmp_week = requests.get('https://www.bsuir.by/schedule/rest/currentWeek/date/' + date)
        week_num = str(tmp_week.content)[2]
        pretext = 'в'
        if tmp_date[6] == 0:
            week_day = 'Понедельник'
        elif tmp_date[6] == 1:
            week_day = 'Вторник'
            pretext = 'во'
        elif tmp_date[6] == 2:
            week_day = 'Среда'
        elif tmp_date[6] == 3:
            week_day = 'Четверг'
        elif tmp_date[6] == 4:
            week_day = 'Пятница'
        elif tmp_date[6] == 5:
            week_day = 'Суббота'
        elif tmp_date[6] == 6:
            week_day = 'Воскресенье'
        schedule += pretext + ' ' + week_day + ':\n \n'

        resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/' + str(group))
        soup = Soup(resp.content)
        day = soup.findAll('weekDay', text=week_day)
        if not day:
            return 'занятий нет, иди катать'

        day = day[0].findParent('scheduleModel')
        subs = day.findAll('weekNumber', text=week_num)
        if not subs:
            return 'занятий нет, иди катать'

        for subject in subs:
            subject = subject.findParent('schedule')
            schedule += (subject.lessonTime.text + ' ' +
                         subject.subject.text + ' (' +
                         subject.lessonType.text + ')')
            if subject.auditory is not None:
                schedule += ' ' + subject.auditory.text
            if subject.numSubgroup.text != '0':
                schedule += ' (' + subject.numSubgroup.text + ')'
            if subject.lastName is not None and subject.numSubgroup.text == '0':
                schedule += ' ' + subject.lastName.text
            schedule += '\n\n'

        return schedule
   