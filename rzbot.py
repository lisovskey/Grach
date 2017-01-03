# -*- coding: utf-8 -*-
'''
работаем
'''
import API
import requests
from datetime import datetime, date, time, timedelta
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
        
    def getSchedule(group, d):
    # schedule takes group and delta days and returns day's schedule
        sub = ""
        date = ""
        tmpDate = datetime.now() + timedelta(days=d)
        tmpDate = tmpDate.timetuple()
        date += str(tmpDate[2]) + "." + str(tmpDate[1]) + "." + str(tmpDate[0])
        wn = requests.get("https://www.bsuir.by/schedule/rest/currentWeek/date/" + date)
        weekNum = str(wn.content)[2]
        if tmpDate[6] == 0:
            weekDay = "Понедельник"
        elif tmpDate[6] == 1:
            weekDay = "Вторник"
        elif tmpDate[6] == 2:
            weekDay = "Среда"
        elif tmpDate[6] == 3:
            weekDay = "Четверг"
        elif tmpDate[6] == 4:
            weekDay = "Пятница"
        elif tmpDate[6] == 5:
            weekDay = "Суббота"
        elif tmpDate[6] == 6:
            weekDay = "Воскресенье"
        sub += weekDay + "\n"
        resp = requests.get("https://www.bsuir.by/schedule/rest/schedule/" + group)
        soup = Soup(resp.content)
        day = soup.findAll("weekDay", text=weekDay)
        if not day:
            return "Занятий нет, иди катать"
        day = day[0].findParent("scheduleModel")
        subs = day.findAll("weekNumber", text=weekNum)
        if not subs:
            return "Занятий нет, иди катать"
        for subI in subs:
            subI = subI.findParent("schedule")
            sub += subI.lessonTime.text + " " + subI.subject.text + " " + subI.lessonType.text
            if subI.auditory is not None:
                sub += " " + subI.auditory.text
            if subI.numSubgroup.text != "0":
                sub += " (" + subI.numSubgroup.text + ")"
            if subI.lastName is not None and subI.numSubgroup.text == "0":
                sub += " " + subI.lastName.text
            sub += "\n"
        return sub
