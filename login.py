#!/usr/bin/python3
# coding: utf-8

import os
import csv

class init(object):
    """ récupère les identifiants dans un fichier séparé """
    def __init__(self):

        with open('identifiant.conf') as csvfile:
            idReader = csv.reader(csvfile, delimiter=";", quotechar='"', )
            for row in idReader: 
                if row[0] == 'IDBOT':
                    self.bot = row[1]
                elif row[0] == 'IDCHAT':
                    self.chatID = row[1]
                elif row[0] == 'HORIZON':
                    self.horizon = row[1]
                elif row[0] == 'LATITUDE':
                    self.latitude = row[1]
                elif row[0] == 'LONGITUDE':
                    self.longitude = row[1]
                elif row[0] == 'GPIOUP':
                    self.gpioUp = row[1]
                elif row[0] == 'GPIODOWN':
                    self.gpioDown = row[1]
                elif row[0] == 'GPIOUPCTRL':
                    self.gpioUpCtrl = row[1]
                elif row[0] == 'GPIODOWNCTRL':
                    self.gpioDownCtrl = row[1]
                elif row[0] == 'LENGTHUP':
                    self.lengthUp = row[1]
                elif row[0] == 'LENGTHDOWN':
                    self.lentghDown = row[1]
                elif row[0] == 'NAME':
                    self.name = row[1]
        

if __name__ == '__main__': 
    id = init()
    print(id.bot)
    print(id.chatID)
    print(id.horizon)
    print(id.latitude)
    print(id.longitude)
    print(id.gpioUp)
    print(id.gpioDown)
    print(id.name)



