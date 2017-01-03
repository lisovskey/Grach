'''
работаем
'''
from datetime import datetime, date, time, timedelta
import API
import requests
from bs4 import BeautifulStoneSoup as Soup

class RZTeleBot(API.TeleBot):
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
        sub = ''
        date = ''
        tmp_date = datetime.now() + timedelta(days=delta)
        tmp_date = tmp_date.timetuple()
        date += str(tmp_date[2]) + '.' + str(tmp_date[1]) + '.' + str(tmp_date[0])
        wn = requests.get('https://www.bsuir.by/schedule/rest/currentWeek/date/' + date)
        week_num = str(wn.content)[2]
        if tmp_date[6] == 0:
            week_day = 'Понедельник'
        elif tmp_date[6] == 1:
            week_day = 'Вторник'
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
        sub += week_day + '\n'
        resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/' + group)
        soup = Soup(resp.content)
        day = soup.findAll('week_day', text=week_day)
        if not day:
            return 'занятий нет, иди катать'
        day = day[0].findParent('scheduleModel')
        subs = day.findAll('week_number', text=week_num)
        if not subs:
            return 'занятий нет, иди катать'
        for subI in subs:
            subI = subI.findParent('schedule')
            sub += subI.lessonTime.text + ' ' + subI.subject.text + ' ' + subI.lessonType.text
            if subI.auditory is not None:
                sub += ' ' + subI.auditory.text
            if subI.numSubgroup.text != '0':
                sub += ' (' + subI.numSubgroup.text + ')'
            if subI.lastName is not None and subI.numSubgroup.text == '0':
                sub += ' ' + subI.lastName.text
            sub += '\n'
        return sub
