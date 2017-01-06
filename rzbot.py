# -*- coding: utf-8 -*-

'''
работаем
'''

from datetime import datetime, timedelta
import telebot
import requests
from bs4 import BeautifulStoneSoup as Soup


class RZTeleBot(telebot.TeleBot):
    '''
    ну это типа грач
    '''
    interlocutor_id = int
    def __init__(self, token):
        '''
        создаем грача
        '''
        super().__init__(token)
        self.interlocutor_id = 0
        print(self.get_me())

    def log_message(self, received_message, answer):
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

    def reply(self, received_message, send_what, answer):
        '''
        посылаем с логом
        '''
        self.log_message(received_message, answer)
        send_what(received_message.chat.id, answer)

    def get_schedule(self, group, delta):
        '''
        schedule takes group and delta days and returns day's schedule
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
        schedule += pretext + ' ' + tmp_week + ':\n \n'

        resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/' + str(group))
        soup = Soup(resp.content)
        day = soup.findAll('weekDay', text=week_day)
        if not day:
            return 'нет у тебя пар'

        day = day[0].findParent('scheduleModel')
        subs = day.findAll('weekNumber', text=week_num)
        if not subs:
            return 'нет у тебя пар'

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
    
    
    def calculate(self, text_message):
        answer = None
        numbers = []
        for num in text_message.split():
            try:
                numbers.append(float(num))
            except ValueError:
                pass
        if not numbers:
            return 'чота херня какаята, введи так: \n[первое] (тут пробел) [чо хочешь] (тут тоже пробел) [второе]'
        print(numbers)
        try:
            if 'умнож' in text_message or '*' in text_message:
                answer = round(numbers[0] * numbers[1])
            elif 'дели' in text_message or '/' in text_message:
                answer = round(numbers[0] / numbers[1], 3)
            elif 'плюс' in text_message or 'слож' in text_message or '+' in text_message:
                answer = round(numbers[0] + numbers[1])
            elif 'минус' in text_message or 'отним' in text_message or '-' in text_message:
                answer = round(numbers[0] - numbers[1])
            elif 'остаток' in text_message or '%' in text_message:
                answer = round(numbers[0] % numbers[1])
        except IndexError:
            answer = 'чота херня какаята\nвведи такЖ [первое] (тут пробел) [чо хочешь] (тут тоже пробел) [второе]'
        return answer
