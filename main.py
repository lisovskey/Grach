'''
умеет мало
работаем дальше
надо в рзбот перенести все
'''

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

        if any(item in text_message for item in constants.TO_HI):
            answer = constants.HI

        elif any(item in text_message for item in constants.TO_BYE):
            answer = constants.BYE

        if ('умееш' in text_message or
            'можеш' in text_message) and (
                '?' in text_message or
                'че' in text_message or
                'чё' in text_message or
                'чо' in text_message or
                'что' in text_message):
            answer = constants.HELP

        elif ('хуй' in text_message or
              'член' in text_message) and (
                  'василюк' in text_message or
                  'денис' in text_message or
                  'покажи' in text_message or
                  'скинь' in text_message):
            answer = constants.DICK
            text = False
            photo = True

        elif ('отсюда' in text_message or
              'отсюдо' in text_message) and (
                  'нахуй' in text_message or
                  'на хуй' in text_message or
                  'нахер' in text_message or
                  'на хер' in text_message):
            if message.chat.id != message.from_user.id:
                answer = constants.OKAY
                leave = True
            else:
                answer = constants.NO

        if any(item == text_message for item in constants.NAMES):
            answer = constants.WHAT

        bot.log(message, answer)

        if photo:
            bot.send_photo(message.chat.id, answer)
        if text:
            bot.send_message(message.chat.id, answer)
        if leave:
            bot.leave_chat(message.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
