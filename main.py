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
    text_message = message.text.lower()
    text_message = text_message.replace('ё', 'е') + ' '
    no_commands = True
    reaction = False
    parts = 0

    if message.chat.id == message.from_user.id:
        reaction = True
    else:
        for name in DATABASE['config']['bot_names']:
            if name in text_message:
                text_message = text_message.replace(name, '')
                bot.interlocutor_id = message.from_user.id
                reaction = True
                break
            elif message.from_user.id == bot.interlocutor_id:
                bot.interlocutor_id = 0
                reaction = True
                break

    if reaction:
        for command in DATABASE['commands']:                                    # start searching for command
            for text in command['text']:                                        #
                for word in text['part']:                                       # start checking command text part
                    if word in text_message:                                    # if subline with command word in message
                        right = True                                            # word is right
                        i = text_message.find(word)                             # find out subline in message
                        length = text_message.find(' ', i)                      # and save its length
                        for exception in command['exceptions']:                 # start checking for exception
                            if exception in text_message[i: length]:            # if exception in subline
                                right = False                                   # word isn't right
                                break                                           # end checking exceptions
                        if right:                                               # if word is right
                            parts += 1                                          # increment phrase parts
                            break                                               # end checking command text part
            if parts == command['parts']:                                       # if phrase parts equals command parts
                no_commands = False                                             #
                exec(command['method'])                                         # do command
                break                                                           # end search for command
            parts = 0                                                           # set to zero phrase parts

        if no_commands:
            if len(text_message) < 4:
                bot.reply(message, bot.send_message,
                          random.choice(DATABASE['config']['bot_call_answer']))
            else:
                bot.reply(message, bot.send_message,
                          DATABASE['config']['bot_ignorance'])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
