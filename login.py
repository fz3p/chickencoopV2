#!/usr/bin/python3
# coding: utf-8

import os
import sys
import csv

class init(object):
    """ récupère les identifiants dans un fichier séparé

    - bot : identifiant du bot Telegram
    - chatID : identifiant du chat Telegram
    - horizon : choix l'horizon
    - latitude : en fonction de la localisation souhaité
    - longitude : en fonction de la localisation souhaité
    - gpioUp : numéro du GPIO pour la montée de la porte
    - gpioDown : numéro du GPIO pour la descente de la porte
    - gpioUpCtrl : numéro du GPIO pour le capteur de fin course de la montée
    - gpioDownCtrl : numéro du GPIO pour le capteur de fin de course de la descente
    - lengthUp : temps d'action du moteur pour la montée
    - lengthDown : temps d'action du moteur pour la descente
    - name : nom du poulailler.
    """
    def __init__(self):

        path = os.path.dirname(sys.argv[0])+'/configuration.conf'
        if path == '/configuration.conf':
            path = "configuration.conf"
        with open(path) as csvfile:
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
                    self.gpioUp = int(row[1])
                elif row[0] == 'GPIODOWN':
                    self.gpioDown = int(row[1])
                elif row[0] == 'GPIOUPCTRL':
                    self.gpioUpCtrl = int(row[1])
                elif row[0] == 'GPIODOWNCTRL':
                    self.gpioDownCtrl = int(row[1])
                elif row[0] == 'LENGTHUP':
                    self.lengthUp = int(row[1])
                elif row[0] == 'LENGTHDOWN':
                    self.lengthDown = int(row[1])
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
    print(id.gpioUpCtrl)
    print(id.gpioDownCtrl)
    print(id.lengthUp)
    print(id.lengthDown)
    print(id.name)



