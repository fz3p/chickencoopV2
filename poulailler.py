#!/usr/bin/python3
# coding: utf-8

import chickenhouse
import telegram
from time import sleep
from datetime import datetime

def modifieState(door, message):
    """ Ouverture/Fermeture de la porte 
    - door : object chickenhouse
    - message : object telegram
    """
    
    # On calcule le temps d'attente avant la prochain action
    liste = [coq.lever.timestamp(), coq.coucher.timestamp()]
    liste.sort()
    wait = int(liste[0]) - int(datetime.now().timestamp())
    
    # on met le programe en pause
    sleep(wait+15)

    # statut de la porte souhaité
    door.stateDoor()

    # controle et changement si nécessaire
    if door.porte == 'opened':
        print("ouverture de la porte")
        door.open()
        message.send("Ouverture de la porte de : " + door.nom)
    elif door.porte == 'closed':
        door.close()
        message.send("fermeture de la porte de : " + door.nom)

# chargement des identifiants, du poulailler, 
coq = chickenhouse.init()
message = telegram.init()

# changement de statut de la porte
modifieState(coq, message)

