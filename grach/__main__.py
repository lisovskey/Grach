# -*- coding: utf-8 -*-

'''
здеся обработчики команд
'''

from os import path, getcwd
import random
import json
import itertools
from . import config, bot, unloader

__location__ = path.join(getcwd(), path.dirname(__file__))
with open(path.join(__location__, 'content.json'), encoding='utf-8') as json_data:
    DATABASE = json.load(json_data)

try:
    grach = bot.Bot(config.TOKEN)
except bot.telebot.apihelper.ApiException:
    print('invalid token error')
    exit(1)


@grach.message_handler(commands=['help', 'start'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    answer = DATABASE['dictionary']['help']
    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['schedule'])
def handle_schedule(message, text_message=None):
    '''
    чо делать, если шедуле
    '''
    answer = ''

    delta = 1
    if text_message != None:
        if any(word in text_message for word in DATABASE['dictionary']['today']):
            delta = 0
        elif any(word in text_message for word in DATABASE['dictionary']['after_tomorrow']):
            delta = 2

    for user in DATABASE['users']:
        if user['name'] == message.from_user.username:
            answer = user['group'] + unloader.get_schedule(user['group_id'], delta)
            break
    else:
        answer = DATABASE['dictionary']['devotion']

    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['cinema'])
def handle_cinema(message, text_message=None):
    '''
    чо делать, если синема
    '''
    answer = DATABASE['dictionary']['solving']
    grach.reply(message, grach.send_message, answer)

    delta = 0
    if text_message != None:
        if any(word in text_message for word in DATABASE['dictionary']['tomorrow']):
            delta = 1
        elif any(word in text_message for word in DATABASE['dictionary']['after_tomorrow']):
            delta = 2

    answer = unloader.get_films(delta)
    grach.reply(message, grach.send_message, answer)

@grach.message_handler(commands=['leave'])
def handle_leave(message):
    '''
    чо делать, если лив
    '''
    answer = ''
    admin = False

    if message.chat.type == 'private':
        answer = DATABASE['dictionary']['negation']
    else:
        if any(user['name'] == message.from_user.username for user in DATABASE['users']):
            answer = DATABASE['dictionary']['obedience']
            admin = True
        else:
            answer = DATABASE['dictionary']['devotion']

    grach.reply(message, grach.send_message, answer)

    if admin:
        grach.leave_chat(message.chat.id)


@grach.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    '''
    чо делать, если шатдаун
    '''
    answer = ''
    admin = False

    if any(user['name'] == message.from_user.username for user in DATABASE['users']):
        answer = DATABASE['dictionary']['obedience']
        admin = True
    else:
        answer = DATABASE['dictionary']['devotion']

    grach.reply(message, grach.send_message, answer)

    if admin:
        grach.stop_polling()
        exit(0)


@grach.message_handler(content_types=['sticker'])
def handle_sticker(message):
    '''
    чо делать, если стикос
    '''
    grach.reply(message, grach.send_sticker, DATABASE['dictionary']['overload'])


@grach.message_handler(content_types=['text'])
def handle_text(message):
    '''
    чо делать, если текст
    '''
    # lower string
    text_message = ' ' + message.text.lower().replace('ё', 'е') + ' '
    # cut rows of identical chars
    text_message = ''.join(ch for ch, _ in itertools.groupby(text_message))

    reaction = False
    parts = 0
    call = ''

    for name in DATABASE['dictionary']['names']:
        if name in text_message:
            call = name
            break

    # private
    if message.chat.type == 'private':
        reaction = True
        if len(text_message.replace(call, '')) < 6:
            grach.reply(message, grach.send_message,
                        random.choice(DATABASE['dictionary']['call_answers']))
            reaction = False
    # group
    else:
        # interlocutor
        if message.from_user.id == grach.interlocutor_id:
            grach.interlocutor_id = 0
            reaction = True

        if any(name in text_message for name in DATABASE['dictionary']['names']):
            reaction = True
            if len(text_message.replace(call, '')) < 6:
                grach.interlocutor_id = message.from_user.id
                grach.reply(message, grach.send_message,
                            random.choice(DATABASE['dictionary']['call_answers']))
                reaction = False
    if reaction:
        # too few chars
        if len(text_message) < 5:
            grach.reply(message, grach.send_message,
                        random.choice(DATABASE['dictionary']['call_answers']))
            reaction = False
        # too many chars
        elif len(text_message) > 60:
            grach.reply(message, grach.send_sticker,
                        DATABASE['dictionary']['overload'])
            reaction = False

    if reaction:
        # start searching for command
        for command in DATABASE['commands']:
            for text in command['text']:
                # start checking command text part
                for word in text:
                    if word in text_message:
                        # checking for exceptions
                        if not any(exc in text_message for exc in command['exceptions']):
                            parts += 1
                            break
            if parts == len(command['text']):
                exec(command['method'])
                break
            parts = 0
        else:
            grach.reply(message, grach.send_message,
                        DATABASE['dictionary']['ignorance'])


if __name__ == '__main__':
    grach.polling(none_stop=True, timeout=10)
