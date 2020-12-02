#!/usr/bin/python3
# coding: utf-8

import requests

class telegram(object):
    def __init__(self, botToken, botChatID):
        self.token = botToken
        self.chatID = botChatID

    def send(self, message):
        url = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatID + '&parse_mode=Markdown&text=' + message
        toSend = requests.get(url)
        print(url)
        return toSend.json()


if __name__ == '__main__': 
    message = telegram('', '')
    message.send('Test python to telegram')





