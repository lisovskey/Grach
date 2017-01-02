'''
умеет мало
работаем дальше
'''

import API
import constants

bot = API.TeleBot(constants.TOKEN)
print(bot.get_me())

def log(message, answer):
    '''
    логируем в консоль
    '''
    print('----------------------------------------------------------------')
    print('{0} {1} (id {2})'.format(message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.id), end='')
    if message.chat.id != message.from_user.id:
        print(' in {0} (id {1}): '.format(message.chat.title,
                                          message.chat.id))
    else:
        print(': ')
    print(' - {}'.format(message.text))
    print('Отвечаю: ')
    print(' - {}'.format(answer))

@bot.message_handler(commands=['help'])
def handle_help(message):
    '''
    чо делать, если халп
    '''
    answer = constants.HELP
    log(message, answer)
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
        if ('грач' in text_message or
            'гриша' in text_message or
            'григорий' in text_message):
            reaction = True
    else:
        reaction = True

    text = False
    photo = False
    leave = False

    if reaction:

        if ('прив' in text_message or
            'привет' in text_message or
            'здравствуй' in text_message or
            'хай' in text_message or
            'хаюх' in text_message or
            'хаю хай' in text_message or
            'дратут' in text_message or
            'здаров' in text_message):
            answer = constants.HI
            text = True

        elif ('все давай' in text_message or
              'всё давай' in text_message or
              'датвиданья' in text_message or
              'до связи' in text_message or
              'до свидани' in text_message or
              'досвидан' in text_message or (
                  'пока' in text_message and
                  'покаж' not in text_message) or (
                      'пака' in text_message and
                      'пакаж' not in text_message)):
            answer = constants.BYE
            text = True

        if ('умееш' in text_message or
            'можеш' in text_message) and (
                '?' in text_message or
                'че' in text_message or
                'чё' in text_message or
                'чо' in text_message or
                'что' in text_message):
            answer = constants.HELP
            text = True

        elif ('хуй' in text_message or
              'член' in text_message) and (
                  'василюк' in text_message or
                  'денис' in text_message or
                  'покажи' in text_message or
                  'скинь' in text_message):
            answer = constants.DICK
            photo = True

        elif ('отсюда' in text_message or
              'отсюдо' in text_message) and (
                  'нахуй' in text_message or
                  'на хуй' in text_message or
                  'нахер' in text_message or
                  'на хер' in text_message):
            if message.chat.id != message.from_user.id:
                answer = constants.BYE
                leave = True
            else:
                answer = constants.NO
                text = True

        if (text_message == 'грач' or
            text_message == 'гриша' or
            text_message == 'григорий'):
            answer = constants.WHAT
            text = True

        log(message, answer)

        if photo:
            bot.send_photo(message.chat.id, answer)
        if text:
            bot.send_message(message.chat.id, answer)
        if leave:
            bot.leave_chat(message.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
