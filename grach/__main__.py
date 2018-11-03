'''
the bot and his handlers
'''

from os import path, getcwd, environ
from random import choice, randint
import json
import logging
import itertools
from . import bot, unloader


__location__ = path.join(getcwd(), path.dirname(__file__), 'content')


def load_json(filename):
    with open(path.join(__location__, filename), encoding='utf-8') as data:
        return json.load(data)


COMMANDBASE = load_json('commands.json')
USERBASE = load_json('users.json')
DICTBASE = load_json('dictionary.json')
CRYPTOBASE = load_json('crypto.json')
CONFIGBASE = load_json('config.json')

try:
    grach = bot.Bot(environ['TOKEN'])
except bot.telebot.apihelper.ApiException:
    print('invalid token error')
    exit(1)


def check_reaction(message, text_message):
    '''
    return True if reaction is necessary
    '''
    if message.chat.type == 'private':
        return True
    elif (text_message and
          any(name in text_message for name in DICTBASE['names'])):
        return True
    elif message.from_user.id == grach.interlocutor_id:
        grach.interlocutor_id = 0
        return True
    return False


@grach.message_handler(commands=['help', 'start'])
def handle_help(message):
    '''
    send help text
    '''
    answer = choice(DICTBASE['help'])
    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['schedule'])
def handle_schedule(message, text_message=None,
                    failure_answer=choice(DICTBASE['negation'])):
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
            answer = unloader.get_schedule(user['group'], delta)
            if answer is None:
                answer = failure_answer
            break
    else:
        answer = choice(DICTBASE['devotion'])
    grach.reply(message, grach.send_message, answer)


@grach.message_handler(commands=['cinema'])
def handle_cinema(message, text_message=None,
                  failure_answer=choice(DICTBASE['negation'])):
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
def handle_crypto(message, text_message=None,
                  failure_answer=choice(DICTBASE['negation'])):
    '''
    send cryptocurrency exchange rates in usd
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


@grach.message_handler(commands=['weather'])
def handle_weather(message, text_message=None,
                   failure_answer=choice(DICTBASE['negation'])):
    '''
    send current weather information
    '''
    answer = unloader.get_weather()
    grach.reply(message, grach.send_message, answer or failure_answer)


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


@grach.message_handler(content_types=['sticker'])
def handle_sticker(message):
    '''
    send sticker if sticker recieved
    '''
    if check_reaction(message, message.text):
        grach.reply(message, grach.send_sticker, choice(DICTBASE['overload']))


@grach.message_handler(content_types=['text'])
def handle_text(message):
    '''
    send message if message recieved depends on who, what and where sent it
    '''
    def useful_text_len(text_message):
        '''
        return len of message without bot name
        '''
        call = ''
        for name in DICTBASE['names']:
            if name in text_message:
                call = name
                break
        return len(text_message.replace(call, '').strip())


    def check_recognition(message, text_message):
        '''
        return True if database check is necessary
        '''
        text_len = useful_text_len(text_message)
        if message.chat.type == 'private':
            if text_len < CONFIGBASE['min_len']:
                return False
        elif (any(name in text_message for name in DICTBASE['names']) and
            text_len < CONFIGBASE['min_len']):
            grach.interlocutor_id = message.from_user.id
            return False
        return True


    def process_text_message(text_message):
        '''
        lower, unstripe, cut rows of identical chars
        '''
        text_message = ' ' + text_message.lower().replace('ё', 'е') + ' '
        return ''.join(ch for ch, _ in itertools.groupby(text_message))


    def find_command(text_message):
        '''
        execute command if found in commandbase
        '''
        for command in COMMANDBASE:
            parts = 0
            for text in command['text']:
                for word in text:
                    if word in text_message:
                        if not any(exc in text_message for exc in command['exceptions']):
                            parts += 1
                            break
            if parts == len(command['text']):
                return command['method'], choice(command['answers'])
        return None, None


    text_message = process_text_message(message.text)
    if check_reaction(message, text_message):
        if check_recognition(message, text_message):
            if useful_text_len(text_message) < CONFIGBASE['min_len']:
                grach.reply(message, grach.send_message,
                            choice(DICTBASE['call_answers']))
            elif len(text_message) > CONFIGBASE['max_len']:
                grach.reply(message, grach.send_sticker,
                            choice(DICTBASE['overload']))
            else:
                command, answer = find_command(text_message)
                if command:
                    # omg facepalm
                    exec(command)
                else:
                    grach.reply(message, grach.send_message,
                                choice(DICTBASE['incomprehension']))
        else:
            grach.reply(message, grach.send_message,
                        choice(DICTBASE['call_answers']))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    grach.polling(none_stop=True, timeout=10)
