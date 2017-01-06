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


@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    for command in DATABASE['commands']:
        if command['title'] == 'help':
            answer = command['answer']
            break

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


@bot.message_handler(content_types=['text'])
def handle_text(message):
    '''
    чо делать, если текст
    '''
    answer = DATABASE['config']['bot_ignorance']
    text_message = message.text.lower()
    text_message = text_message.replace('ё', 'е') + ' '
    no_commands = True
    need_name = True
    parts = 0

    if message.chat.id == message.from_user.id:
        need_name = False
    else:
        if any(name in text_message for name in DATABASE['config']['bot_names']):
            bot.interlocutor_id = message.from_user.id
            need_name = False
        elif bot.interlocutor_id == message.from_user.id:
            need_name = False
        elif (bot.interlocutor_id != message.from_user.id) and any(name in text_message for name in DATABASE['config']['bot_names']):
            bot.interlocutor_id = message.from_user.id
            need_name = False
        else:
            bot.interlocutor_id = 0
            need_name = True
        '''message.from_user.id == bot.interlocutor_id:
            bot.interlocutor_id = 0
            need_name = False'''

    for command in DATABASE['commands']:
        for text in command['text']:
            for word in text['part']:
                if word in text_message:
                    right = True
                    i = text_message.find(word)
                    length = text_message.find(' ', i)
                    for exception in command['exceptions']:
                        if exception in text_message[i: length]:
                            right = False
                            break
                    if right:
                        parts += 1
                        break
        if not need_name:
            if parts == command['parts']:
                no_commands = False
                exec(command['method'])
                break
        parts = 0

    if no_commands and not need_name:
        bot.reply(message, bot.send_message, random.choice(DATABASE['config']['bot_call_answer']))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
