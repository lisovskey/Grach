# -*- coding: utf-8 -*-

'''
the bot and his handlers
'''

from os import path, getcwd
from random import choice, randint
import json
import itertools
from . import config, bot, unloader


__location__ = path.join(getcwd(), path.dirname(__file__), 'content')
with open(path.join(__location__, 'commands.json'), encoding='utf-8') as json_data:
    COMMANDBASE = json.load(json_data)
with open(path.join(__location__, 'users.json'), encoding='utf-8') as json_data:
    USERBASE = json.load(json_data)
with open(path.join(__location__, 'dictionary.json'), encoding='utf-8') as json_data:
    DICTBASE = json.load(json_data)
with open(path.join(__location__, 'crypto.json'), encoding='utf-8') as json_data:
    CRYPTOBASE = json.load(json_data)

try:
    grach = bot.Bot(config.TOKEN)
except bot.telebot.apihelper.ApiException:
    print('invalid token error')
    exit(1)


@grach.message_handler(commands=['help', 'start'])
def handle_help(message):
    '''
    send help text
    '''
    answer = choice(DICTBASE['help'])
    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['schedule'])
def handle_schedule(message, text_message=None, failure_answer=choice(DICTBASE['negation'])):
    '''
    send bsuir schedule if user in userbase
    '''
    delta = 1
    if text_message is not None:
        if any(word in text_message for word in DICTBASE['today']):
            delta = 0
        elif any(word in text_message for word in DICTBASE['after_tomorrow']):
            delta = 2

    for user in USERBASE:
        if user['name'] == message.from_user.username:
            schedule = unloader.get_schedule(user['group'], delta)
            if schedule is not None:
                answer = user['group'] + schedule
            else:
                answer = failure_answer
            break

    else:
        answer = choice(DICTBASE['devotion'])
    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['cinema'])
def handle_cinema(message, text_message=None, failure_answer=choice(DICTBASE['negation'])):
    '''
    send list of films at the minsk box office
    '''
    answer = choice(DICTBASE['solving'])
    grach.reply(message, grach.send_message, answer)

    delta = 0
    if text_message is not None:
        if any(word in text_message for word in DICTBASE['tomorrow']):
            delta = 1
        elif any(word in text_message for word in DICTBASE['after_tomorrow']):
            delta = 2

    answer = unloader.get_films(delta)
    if answer is None:
        answer = failure_answer

    grach.reply(message, grach.send_message, answer)

@grach.message_handler(commands=['crypto'])
def handle_crypto(message, text_message=None, failure_answer=choice(DICTBASE['negation'])):
    '''
    send cryptocurrency exchange retes in usd
    '''
    currency_name = 'error'

    if text_message is not None:
        for currency in CRYPTOBASE:
            if any(name in text_message for name in currency['verbose_names']):
                currency_name = currency['name']
                break
    else:
        currency_name = CRYPTOBASE[0]['name']

    answer = unloader.get_cryptorate(currency_name)
    if answer is None:
        answer = failure_answer
    else:
        answer += ' ' + choice(DICTBASE['dollars'])

    grach.reply(message, grach.send_message, answer)

@grach.message_handler(commands=['leave'])
def handle_leave(message, failure_answer=choice(DICTBASE['negation'])):
    '''
    leave chat if user in userbase and if possible
    '''
    admin = False

    if (message.chat.type != 'private' and
            any(user['name'] == message.from_user.username for user in USERBASE)):
        answer = choice(DICTBASE['obedience'])
        admin = True
    else:
        answer = failure_answer

    grach.reply(message, grach.send_message, answer)

    if admin:
        grach.leave_chat(message.chat.id)


@grach.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    '''
    shutdown if user in userbase
    '''
    admin = False

    if any(user['name'] == message.from_user.username for user in USERBASE):
        answer = choice(DICTBASE['obedience'])
        admin = True
    else:
        answer = choice(DICTBASE['devotion'])

    grach.reply(message, grach.send_message, answer)

    if admin:
        grach.stop_polling()
        exit(0)


@grach.message_handler(content_types=['sticker'])
def handle_sticker(message):
    '''
    send sticker if sticker recieved
    '''
    grach.reply(message, grach.send_sticker, choice(DICTBASE['overload']))


@grach.message_handler(content_types=['text'])
def handle_text(message):
    '''
    send message if message recieved depends on who, what and where sent it
    '''
    # lower string
    text_message = ' ' + message.text.lower().replace('ё', 'е') + ' '
    # cut rows of identical chars
    text_message = ''.join(ch for ch, _ in itertools.groupby(text_message))

    reaction = False
    parts = 0
    call = ''

    for name in DICTBASE['names']:
        if name in text_message:
            call = name
            break

    # private
    if message.chat.type == 'private':
        reaction = True
        if len(text_message.replace(call, '')) < 6:
            grach.reply(message, grach.send_message,
                        choice(DICTBASE['call_answers']))
            reaction = False
    # group
    else:
        # interlocutor
        if message.from_user.id == grach.interlocutor_id:
            grach.interlocutor_id = 0
            reaction = True

        if any(name in text_message for name in DICTBASE['names']):
            reaction = True
            if len(text_message.replace(call, '')) < 6:
                grach.interlocutor_id = message.from_user.id
                grach.reply(message, grach.send_message, choice(DICTBASE['call_answers']))
                reaction = False
    if reaction:
        # too few chars
        if len(text_message) < 5:
            grach.reply(message, grach.send_message, choice(DICTBASE['call_answers']))
            reaction = False
        # too many chars
        elif len(text_message) > 60:
            grach.reply(message, grach.send_sticker, choice(DICTBASE['overload']))
            reaction = False

    if reaction:
        # start searching for command
        for command in COMMANDBASE:
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
            grach.reply(message, grach.send_message, choice(DICTBASE['incomprehension']))


if __name__ == '__main__':
    grach.polling(none_stop=True, timeout=10)
