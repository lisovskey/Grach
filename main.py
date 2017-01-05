# -*- coding: utf-8 -*-

'''
умеет мало
работаем дальше
надо в рзбот перенести все
'''

from contextlib import redirect_stderr
import sys
import random
import json
import rzbot
import phrases
import files

with open('content.json') as json_data:
    DATABASE = json.load(json_data)

with open('errors.log', 'w') as stderr, redirect_stderr(stderr):
    bot = rzbot.RZTeleBot(DATABASE['config']['token'])

    @bot.message_handler(commands=['shutdown'])
    def handle_shutdown(message):
        '''
        чо делать, если шатдаун
        '''
        shutdown = False

        try:
            for user in DATABASE['users']:
                if user['name'] == message.from_user.username:
                    answer = random.choice(phrases.OKAY_LIST)
                    shutdown = True
        except KeyError:
            answer = phrases.UNKNOWN_USER

        bot.log_message(message, answer)
        bot.send_message(message.chat.id, answer)

        if shutdown:
            sys.exit(0)


    @bot.message_handler(commands=['help'])
    def handle_help(message):
        '''
        чо делать, если халп
        '''
        answer = phrases.HELP
        bot.log_message(message, answer)
        bot.send_message(message.chat.id, answer)


    @bot.message_handler(commands=['schedule'])
    def handle_schedule(message):
        '''
        чо делать, если шедуле
        '''
        answer = ''
        try:
            for user in DATABASE['users']:
                if user['name'] == message.from_user.username:
                    answer = user['group'] + ' ' +  bot.get_schedule(user['id'], 1)
        except KeyError:
            answer = phrases.UNKNOWN_USER
        bot.log_message(message, answer)
        bot.send_message(message.chat.id, answer)


    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        '''
        как отвечать
        '''
        answer = phrases.IGNORANCE
        text_message = message.text.lower()

        reaction = False
        if message.chat.id != message.from_user.id:
            if any(item in text_message for item in phrases.NAMES):
                reaction = True
        else:
            reaction = True

        text = True
        photo = False
        leave = False

        if reaction:

            if (any(item in text_message for item in phrases.TO_HI) and not
                any(item in text_message for item in phrases.NOT_TO_HI)):
                answer = random.choice(phrases.HI_LIST)

            elif (any(item in text_message for item in phrases.TO_BYE) and not
                any(item in text_message for item in phrases.NOT_TO_BYE)):
                answer = random.choice(phrases.BYE_LIST)

            if (any(item in text_message for item in phrases.TO_SCHEDULE_1) and
                any(item in text_message for item in phrases.TO_SCHEDULE_2) and not
                any(item in text_message for item in phrases.NOT_TO_SCHEDULE)):
                answer = phrases.UNKNOWN_USER
            elif (any(item in text_message for item in phrases.TO_HELP_1) and
                any(item in text_message for item in phrases.TO_HELP_2)):
                answer = phrases.HELP

            elif (any(item in text_message for item in phrases.TO_DICK_1) and
                any(item in text_message for item in phrases.TO_DICK_2)):
                answer = files.DICK
                text = False
                photo = True

            elif (any(item in text_message for item in phrases.TO_LEAVE_1) and
                any(item in text_message for item in phrases.TO_LEAVE_2)):
                if message.chat.id != message.from_user.id:
                    answer = random.choice(phrases.OKAY_LIST)
                    leave = True
                else:
                    answer = random.choice(phrases.NO_LIST)

            if any(item == text_message for item in phrases.NAMES):
                answer = random.choice(phrases.WHAT_LIST)

            bot.log_message(message, answer)

            if text:
                bot.send_message(message.chat.id, answer)
            if photo:
                bot.send_photo(message.chat.id, answer)
            if leave:
                bot.leave_chat(message.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
