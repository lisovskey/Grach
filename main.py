# -*- coding: utf-8 -*-
'''
умеет мало
работаем дальше
надо в рзбот перенести все
'''

import random
import rzbot
import constants

bot = rzbot.RZTeleBot(constants.TOKEN)

@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    answer = constants.HELP
    bot.log(message, answer)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['schedule'])
def handle_shedule(message):
    '''
    чо делать, если шедуле
    '''
    answer = bot.get_schedule(614302, 1)
    bot.log(message, answer)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    '''
    как отвечать
    '''
    answer = constants.IGNORANCE
    text_message = message.text.lower()

    reaction = False
    if message.chat.id != message.from_user.id:
        if any(item in text_message for item in constants.NAMES):
            reaction = True
    else:
        reaction = True

    text = True
    photo = False
    leave = False

    if reaction:

        if (any(item in text_message for item in constants.TO_HI) and
            any(item not in text_message for item in constants.NOT_TO_HI)):
            answer = random.choice(constants.HI_LIST)

        elif (any(item in text_message for item in constants.TO_BYE) and
              any(item not in text_message for item in constants.NOT_TO_BYE)):
            answer = random.choice(constants.BYE_LIST)

        if (any(item in text_message for item in constants.TO_HELP_1) and
            any(item in text_message for item in constants.TO_HELP_2)):
            answer = constants.HELP

        elif (any(item in text_message for item in constants.TO_DICK_1) and
              any(item in text_message for item in constants.TO_DICK_2)):
            answer = constants.DICK
            text = False
            photo = True

        elif (any(item in text_message for item in constants.TO_LEAVE_1) and
              any(item in text_message for item in constants.TO_LEAVE_2)):
            if message.chat.id != message.from_user.id:
                answer = random.choice(constants.OKAY_LIST)
                leave = True
            else:
                answer = random.choice(constants.NO_LIST)

        if any(item == text_message for item in constants.NAMES):
            answer = random.choice(constants.WHAT_LIST)

        bot.log(message, answer)

        if text:
            bot.send_message(message.chat.id, answer)
        if photo:
            bot.send_photo(message.chat.id, answer)
        if leave:
            bot.leave_chat(message.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
