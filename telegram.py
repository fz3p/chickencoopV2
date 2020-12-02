#!/usr/bin/python3
# coding: utf-8

import requests

class telegram(object):
    """ permet d'envoyer les messages sur Telegram
    - token : l'identifiant du bot
    - chatID : identifiant du chat
    - send() : envoi un message à Telegram
    """
    def __init__(self, botToken, botChatID):
        """ charge la configuration """
        self.token = botToken
        self.chatID = botChatID

    def send(self, message):
        """ envoi le message au bot """
        url = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatID + '&parse_mode=Markdown&text=' + message
        toSend = requests.get(url)
        print(url)
        return toSend.json()


if __name__ == '__main__': 
    message = telegram('', '')
    message.send('Test python to telegram')





