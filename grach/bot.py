from datetime import datetime
import logging
import telebot


class Bot(telebot.AsyncTeleBot):
    """
    a bot actually
    """
    def __init__(self, token):
        """
        create with logger and last interlocutor id
        """
        super().__init__(token)
        self.interlocutor_id = 0
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)
        logging.info(self.get_me())


    def log_message(self, received_message, answer):
        """
        log to console
        """
        logging.info(' %s\n%s %s (id %s) in %s:\n - %s\nReplying:\n - %s',
                     datetime.now().strftime('%d.%m.%y %H:%M'),
                     received_message.from_user.first_name,
                     received_message.from_user.last_name,
                     received_message.from_user.id,
                     received_message.chat.title or 'private chat',
                     received_message.text,
                     answer)


    def reply(self, received_message, send_what, answer):
        """
        reply with logging
        """
        send_what(received_message.chat.id, answer)
        self.log_message(received_message, answer)
