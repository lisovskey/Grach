# -*- coding: utf-8 -*-

'''
умеет мало
работаем дальше
надо в рзбот перенести все
'''

import sys
import random
import json
import rzbot

with open('content.json') as json_data:
    DATABASE = json.load(json_data)

bot = rzbot.RZTeleBot(DATABASE['config']['bot_token'])


@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    try:
        for user in DATABASE['users']:
            if user['name'] == message.from_user.username:
                for command in DATABASE['commands']:
                    if command['title'] == 'help':
                        answer = random.choice(command['answer'])
                        break
    except KeyError:
        answer = DATABASE['config']['bot_devotion']

    bot.reply(message, bot.send_message, answer)


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
        answer = DATABASE['config']['bot_devotion']

    bot.reply(message, bot.send_message, answer)


@bot.message_handler(commands=['leave'])
def handle_leave(message):
    '''
    чо делать, если лив
    '''
    leave = False
    try:
        for user in DATABASE['users']:
            if user['name'] == message.from_user.username:
                answer = DATABASE['config']['bot_okay']
                leave = True
    except KeyError:
        answer = DATABASE['config']['bot_devotion']

    bot.reply(message, bot.send_message, answer)
    if leave:
        bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    '''
    чо делать, если шатдаун
    '''
    shutdown = False
    try:
        for user in DATABASE['users']:
            if user['name'] == message.from_user.username:
                answer = DATABASE['config']['bot_okay']
                shutdown = True
    except KeyError:
        answer = DATABASE['config']['bot_devotion']

    bot.reply(message, bot.send_message, answer)
    if shutdown:
        sys.exit(0)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    '''
    чо делать, если текст
    '''
    text_message = message.text.lower()
    text_message = text_message.replace('ё', 'е') + ' '
    no_commands = True
    reaction = False
    parts = 0

    # личка
    if message.chat.id == message.from_user.id:
        for name in DATABASE['config']['bot_names']:
            if name in text_message:
                text_message = text_message.replace(name, '')
                break
        reaction = True
    # конфа
    else:
        # собеседник
        if message.from_user.id == bot.interlocutor_id:
            bot.interlocutor_id = 0
            for name in DATABASE['config']['bot_names']:
                if name in text_message:
                    text_message = text_message.replace(name, '')
                    if len(text_message) < 4:
                        bot.interlocutor_id = message.from_user.id
                    break
            reaction = True
        # хер с горы
        else:
            for name in DATABASE['config']['bot_names']:
                if name in text_message:
                    text_message = text_message.replace(name, '')
                    if len(text_message) < 4:
                        bot.interlocutor_id = message.from_user.id
                    reaction = True
                    break

    # много буков
    if reaction and len(text_message) > 50:
        bot.reply(message, bot.send_message,
                  DATABASE['config']['bot_overload'])
        reaction = False

    if reaction:
        # start searching for command
        for command in DATABASE['commands']:
            for text in command['text']:
                # start checking command text part
                for word in text['part']:
                    if word in text_message:
                        right = True
                        i = text_message.find(word)
                        length = text_message.find(' ', i)
                        # start checking for exceptions
                        for exception in command['exceptions']:
                            if exception in text_message[i: length]:
                                right = False
                                break
                        # end checking exceptions
                        if right:
                            parts += 1
                            break
                # end checking command text part
            if parts == command['parts']:
                no_commands = False
                exec(command['method'])
                break
        # end searching for command
            parts = 0

        if no_commands:
            if len(text_message) < 4:
                bot.reply(message, bot.send_message,
                          random.choice(DATABASE['config']['bot_call_answer']))
            else:
                bot.reply(message, bot.send_message,
                          DATABASE['config']['bot_ignorance'])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
