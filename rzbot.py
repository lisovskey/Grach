'''
работаем
'''
import API

class RZTeleBot(API.TeleBot):
    '''
    ну это типа грач
    '''
    def __init__(self, token):
        '''
        создаем грача
        '''
        super().__init__(token)
        print(self.get_me())

    def log(self, received_message, answer):
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

    def reply(self, received_message, send_what, to_chat_id, answer):
        '''
        посылаем с логом
        '''
        self.log(received_message, answer)
        send_what(to_chat_id, answer)
