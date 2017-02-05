# -*- coding: utf-8 -*-

'''
здеся обработчики команд
'''

import os
import random
import json
import itertools
from . import config, bot, unloader

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'content.json'), encoding='utf-8') as json_data:
    DATABASE = json.load(json_data)

try:
    bot = bot.RZTeleBot(config.TOKEN)
    loader = unloader.Unloader()
except bot.telebot.apihelper.ApiException:
    print('invalid token error')
    exit(1)


@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    answer = DATABASE['dictionary']['help']
    bot.reply(message, bot.send_message, answer)


@bot.message_handler(commands=['schedule'])
def handle_schedule(message, text_message=None):
    '''
    чо делать, если шедуле
    '''
    answer = ''
    admin = False

    delta = 1
    if text_message != None:
        if any(word in text_message for word in DATABASE['dictionary']['today']):
            delta = 0
        elif any(word in text_message for word in DATABASE['dictionary']['after_tomorrow']):
            delta = 2

    for user in DATABASE['users']:
        if user['name'] == message.from_user.username:
            answer = user['group'] + loader.get_schedule(user['id'], delta)
            admin = True
            break

    if not admin:
        answer = DATABASE['dictionary']['devotion']

    bot.reply(message, bot.send_message, answer)


@bot.message_handler(commands=['cinema'])
def handle_cinema(message, text_message=None):
    '''
    чо делать, если синема
    '''
    answer = DATABASE['dictionary']['solving']
    bot.reply(message, bot.send_message, answer)

    delta = 1
    if text_message != None:
        if any(word in text_message for word in DATABASE['dictionary']['today']):
            delta = 0
        elif any(word in text_message for word in DATABASE['dictionary']['after_tomorrow']):
            delta = 2

    answer = loader.get_films(delta)
    bot.reply(message, bot.send_message, answer)

@bot.message_handler(commands=['leave'])
def handle_leave(message):
    '''
    чо делать, если лив
    '''
    answer = ''
    admin = False

    if message.chat.id == message.from_user.id:
        answer = DATABASE['dictionary']['negation']
    else:
        if any(user['name'] == message.from_user.username for user in DATABASE['users']):
            answer = DATABASE['dictionary']['obedience']
            admin = True

        if not admin:
            answer = DATABASE['dictionary']['devotion']

    bot.reply(message, bot.send_message, answer)

    if admin:
        bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    '''
    чо делать, если шатдаун
    '''
    answer = ''
    admin = False

    if any(user['name'] == message.from_user.username for user in DATABASE['users']):
        answer = DATABASE['dictionary']['obedience']
        admin = True

    if not admin:
        answer = DATABASE['dictionary']['devotion']

    bot.reply(message, bot.send_message, answer)

    if admin:
        exit(0)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    '''
    чо делать, если стикос
    '''
    print('----------------------------------------------------------------')
    print(message.sticker.file_id)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    '''
    чо делать, если текст
    '''
    # опускаем строку
    text_message = ' ' + message.text.lower().replace('ё', 'е') + ' '
    # обрезаем очередь повторяющихся символов
    text_message = ''.join(ch for ch, _ in itertools.groupby(text_message))

    no_commands = True
    reaction = False
    parts = 0
    call = ''

    for name in DATABASE['dictionary']['names']:
        if name in text_message:
            call = name
            break

    # личка
    if message.chat.id == message.from_user.id:
        reaction = True
        if len(text_message.replace(call, '')) < 6:
            bot.reply(message, bot.send_message,
                      random.choice(DATABASE['dictionary']['call_answers']))
            reaction = False
    # конфа
    else:
        # собеседник
        if message.from_user.id == bot.interlocutor_id:
            bot.interlocutor_id = 0
            reaction = True

        if any(name in text_message for name in DATABASE['dictionary']['names']):
            reaction = True
            if len(text_message.replace(call, '')) < 6:
                bot.interlocutor_id = message.from_user.id
                bot.reply(message, bot.send_message,
                          random.choice(DATABASE['dictionary']['call_answers']))
                reaction = False
    if reaction:
        # мало буков
        if len(text_message) < 5:
            bot.reply(message, bot.send_message,
                      random.choice(DATABASE['dictionary']['call_answers']))
            reaction = False
        # много буков
        elif len(text_message) > 60:
            bot.reply(message, bot.send_sticker,
                      DATABASE['dictionary']['overload'])
            reaction = False

    if reaction:
        # start searching for command
        for command in DATABASE['commands']:
            for text in command['text']:
                # start checking command text part
                for word in text['part']:
                    if word in text_message:
                        # checking for exceptions
                        if not any(exc in text_message for exc in command['exceptions']):
                            parts += 1
                # end checking command text part
            if parts == command['parts']:
                no_commands = False
                exec(command['method'])
                break
        # end searching for command
            parts = 0

        if no_commands:
            bot.reply(message, bot.send_message,
                      DATABASE['dictionary']['ignorance'])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0.5)
