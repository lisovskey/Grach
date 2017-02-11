# -*- coding: utf-8 -*-

'''
работаем жопай
'''

import logging
import math
import telebot

class RZTeleBot(telebot.AsyncTeleBot):
    '''
    ну это типа грач
    '''
    def __init__(self, token):
        '''
        создаем грача
        '''
        super().__init__(token)
        self.interlocutor_id = 0
        logger = telebot.logger
        telebot.logger.setLevel(logging.CRITICAL)
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


    def factorial(self, received_message):
        '''
        считаем факториал
        '''
        text_message = ' ' + received_message.lower().replace('ё', 'е') + ' '
        numbers = []

        if '!' in text_message:
            text_message.replace('!', '')
        for num in text_message.split():
            try:
                numbers.append(float(num))
            except ValueError:
                pass
        if not numbers:
            return 'чо считать дядя'

        if len(numbers) == 1:
            number = int(numbers[0])
            if number < 1001:
                answer = math.factorial(number)
                answer = '{:,}'.format(answer).replace(',', ' ')
                if number > 99:
                    answer += ' но это не точно'
                return answer
            else:
                return 'неенененене'
        else:
            return 'чо считать дядя'
