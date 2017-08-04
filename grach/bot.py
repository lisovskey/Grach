# -*- coding: utf-8 -*-

'''
bot wrapper class
'''

from logging import WARNING
from datetime import datetime
import math
import telebot

class Bot(telebot.TeleBot):
    '''
    a bot actually
    '''
    def __init__(self, token):
        '''
        create with logger and last interlocutor id
        '''
        super().__init__(token)
        self.interlocutor_id = 0
        logger = telebot.logger
        telebot.logger.setLevel(WARNING)
        print(self.get_me())


    def log_message(self, received_message, answer):
        '''
        log to console
        '''
        print(16*'-', str(datetime.now().strftime('%d.%m.%y-%H:%M')), 16*'-')
        print('{} {} (id {})'.format(received_message.from_user.first_name,
                                     received_message.from_user.last_name,
                                     received_message.from_user.id), end='')
        if received_message.chat.type != 'private':
            print(' in {} (id {})'.format(received_message.chat.title,
                                          received_message.chat.id), end='')
        print(': ')
        print(' -', received_message.text)
        print('Отвечаю: ')
        print(' -', answer)


    def reply(self, received_message, send_what, answer):
        '''
        reply with logging
        '''
        self.log_message(received_message, answer)
        send_what(received_message.chat.id, answer)
