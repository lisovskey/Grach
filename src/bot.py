# -*- coding: utf-8 -*-

'''
работаем жопай
'''

import math
import telebot

class RZTeleBot(telebot.TeleBot):
    '''
    ну это типа грач
    '''
    def __init__(self, token):
        '''
        создаем грача
        '''
        super().__init__(token)
        self.interlocutor_id = 0
        print(self.get_me())


    def log_message(self, received_message, answer):
        '''
        логируем в консоль
        '''
        print('----------------------------------------------------------------')
        print('{0} {1} (id {2})'.format(received_message.from_user.first_name,
                                        received_message.from_user.last_name,
                                        received_message.from_user.id), end='')
        if received_message.chat.id != received_message.from_user.id:
            print(' in {0} (id {1}): '.format(received_message.chat.title,
                                              received_message.chat.id))
        else:
            print(': ')
        print(' - {}'.format(received_message.text))
        print('Отвечаю: ')
        print(' - {}'.format(answer))


    def reply(self, received_message, send_what, answer):
        '''
        посылаем с логом
        '''
        self.log_message(received_message, answer)
        send_what(received_message.chat.id, answer)


    def calculate(self, message):
        '''
        6 arithmetic operations
        '''
        text = ' ' + message.lower().replace('ё', 'е') + ' '
        answer = None
        numbers = []
        for num in message.split():
            try:
                numbers.append(float(num))
            except ValueError:
                pass
        if not numbers:
            return 'не могу'

        if len(numbers) == 1 and ('факториал' in text or '!' in text):
            numbers[0] = int(numbers[0])
            if numbers[0] < 1001:
                answer = math.factorial(numbers[0])
                answer = '{:,}'.format(answer).replace(',', ' ')
                if numbers[0] > 100:
                    answer += ' но это не точно'
                return answer
            else:
                return 'неенененене'

        try:
            if 'умнож' in text or '*' in text:
                answer = numbers[0] * numbers[1]
            elif 'дели' in text or '/' in text:
                answer = numbers[0] / numbers[1]
            elif 'плюс' in text or 'слож' in text or '+' in text:
                answer = numbers[0] + numbers[1]
            elif 'минус' in text or 'отним' in text or 'вычт' in text or '-' in text:
                answer = numbers[0] - numbers[1]
            elif 'остаток' in text or '%' in text:
                answer = numbers[0] % numbers[1]
        except IndexError:
            return 'что считать дядя'

        if answer - int(answer) == 0:
            answer = int(answer)
        if answer > 999999999:
            return answer
        else:
            return round(answer, 3)
