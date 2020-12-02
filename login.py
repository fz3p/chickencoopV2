#!/usr/bin/python3
# coding: utf-8

import os
import csv

class login(object):
    """ récupère les identifiants dans un fichier séparé """
    def __init__(self):

        with open('identifiant.conf') as csvfile:
            idReader = csv.reader(csvfile, delimiter=";", quotechar='"', )
            for row in idReader: 
                if row[0] == 'IDBOT':
                    self.bot = row[1]
                elif row[0] == 'IDCHAT':
                    self.chatID = row[1]


if __name__ == '__main__': 
    id = login()
    print(id.bot)
    print(id.chatID)
