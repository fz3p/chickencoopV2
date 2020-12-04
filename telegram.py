#!/usr/bin/python3
# coding: utf-8

import requests
import login

class init(object):
    """ permet d'envoyer les messages sur Telegram
    - bot : l'identifiant du bot
    - chatID : identifiant du chat
    - send() : envoi un message à Telegram
    """
    def __init__(self):
        """ charge la configuration """
        id = login.init()
        self.bot = id.bot
        self.chatID = id.chatID

    def send(self, message):
        """ envoi le message au bot """
        url = 'https://api.telegram.org/bot' + self.bot + '/sendMessage?chat_id=' + self.chatID + '&parse_mode=Markdown&text=' + message
        toSend = requests.get(url)
        return toSend.json()


if __name__ == '__main__': 
    message = init()
    message.send('Test python to telegram')





