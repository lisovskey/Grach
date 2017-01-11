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
import unloader

with open('content.json') as json_data:
    DATABASE = json.load(json_data)

bot = rzbot.RZTeleBot(DATABASE['config']['token'])
loader = unloader.Unloader()


@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    answer = ''
    admin = False
    
    for user in DATABASE['users']:
        if user['name'] == message.from_user.username:
            admin = True
            for command in DATABASE['commands']:
                if command['title'] == 'help':
                    answer = random.choice(command['answer'])
                    break

    if not admin:
        answer = DATABASE['dictionary']['devotion']

    bot.reply(message, bot.send_message, answer)


@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    '''
    чо делать, если шедуле
    '''
    answer = ''
    admin = False

    for user in DATABASE['users']:
        if user['name'] == message.from_user.username:
            answer = user['group'] + ' ' +  loader.get_schedule(user['id'], 1)
            admin = True
            break

    if not admin:
        answer = DATABASE['dictionary']['devotion']

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
        for user in DATABASE['users']:
            if user['name'] == message.from_user.username:
                answer = DATABASE['dictionary']['okay']
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

    for user in DATABASE['users']:
        if user['name'] == message.from_user.username:
            answer = DATABASE['dictionary']['okay']
            admin = True
            b

    if not admin:
        answer = DATABASE['dictionary']['devotion']

    bot.reply(message, bot.send_message, answer)

    if admin:
        sys.exit(0)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    '''
    чо делать, если текст
    '''
    text_message = ' ' + message.text.lower().replace('ё', 'е') + ' '
    no_commands = True
    reaction = False
    parts = 0

    # личка
    if message.chat.id == message.from_user.id:
        reaction = True
    # конфа
    else:
        # собеседник
        if message.from_user.id == bot.interlocutor_id:
            bot.interlocutor_id = 0
            for name in DATABASE['dictionary']['names']:
                if name in text_message:
                    if len(text_message.replace(name, '')) < 5:
                        bot.interlocutor_id = message.from_user.id
                    break
            reaction = True
        # хер с горы
        else:
            for name in DATABASE['dictionary']['names']:
                if name in text_message:
                    if len(text_message.replace(name, '')) < 5:
                        bot.interlocutor_id = message.from_user.id
                    reaction = True
                    break

    # много буков
    if reaction and len(text_message) > 50:
        bot.reply(message, bot.send_message,
                  DATABASE['dictionary']['overload'])
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
                            if exception in text_message[i:length]:
                                right = False
                                break
                        # end checking exceptions
                        if right:
            if len(text_message) < 10:
                            break
                # end checking command text part
            if parts == command['parts']:
                no_commands = False
                exec(command['method'])
                break
        # end searching for command
            parts = 0

        if no_commands:
            if len(text_message) < 10:
                bot.reply(message, bot.send_message,
                          random.choice(DATABASE['dictionary']['call_answers']))
            else:
                bot.reply(message, bot.send_message,
                          DATABASE['dictionary']['ignorance'])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
