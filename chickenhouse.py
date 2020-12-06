#!/usr/bin/python3
# coding: utf-8

import ephem
import re
from datetime import datetime
import time
import os
import login
import RPi.GPIO as gpio
import telegram


class init(object):
	"""docstring for chickenhouse
	
	Attributs
	- id : charge les informations du fichier des identifiants
	- position : intègre la localisation de ephem
	- lever : horaire de lever du soleil
	- coucher : horaire de coucher du soleil
	- heure : heure actuelle
	- porte : état dans lequel la porte devrait être
	- nom : nom du poulailler
	- telegram : charge les informations d'envoi à télégram

	Fonctions
	- stateDoor : indique le statut du prochain évènement
	- open() : ouvre la porte
	- close() : ferme la porte
	- modifieState() : change le statut de la porte à l'heure du prochain évènement
	"""

	def __init__(self):
		""" calcul automatiquement le prochain lever de soleil et le prochain coucher de soleil """
	

		def _listDate(date):
			""" convertir la date ephem en date datetime et rajoute le décalage horaire """
			# recupérationd des éléments de la date
			regex = re.compile(r"(\d{4})/(\d{,})/(\d{1,}) (\d{2}):(\d{2}):(\d{2})")
			match = regex.findall(date)
			# on converti le tuple en liste 
			liste = list(sum(match, ())) 
			l = []
			for d in liste:
			 	l.append(int(str(d)))

			#traitement heure d'été/hiver
			decalageHoraire = time.localtime().tm_hour - time.gmtime().tm_hour
			newDate = datetime(l[0], l[1], l[2], l[3]+decalageHoraire, l[4], l[5])
			return newDate
		
		def _position(self):
			"""	position du poullailler """
			localisation = ephem.Observer()
			localisation.horizon, localisation.lat, localisation.long = self.id.horizon, self.id.latitude, self.id.longitude
			localisation.date = ephem.Date(datetime.now())
			return localisation
		
		def sunrise(self):
			""" lever du soleil """
			hour = self.position.next_rising(ephem._sun)
			return _listDate(str(hour))
		
		def sunset(self):
			""" coucher du soleil """
			hour = self.position.next_setting(ephem._sun)
			return _listDate(str(hour))
		

		self.id = login.init()
		self.position = _position(self)
		self.lever = sunrise(self)
		self.coucher = sunset(self)
		self.heure = datetime.now()
		self.porte = ''
		self.nom = self.id.name
		self.telegram = telegram.init()
		

	def stateDoor(self):
		""" détermine si la porte est ouverte ou fermée en fonction de l'horaire 
		Attention cela est en fonction de la date d'initialisation de l'objet. 
		Sinon cela renvoie le prochain état.
		"""

		if self.lever.timestamp() < datetime.now().timestamp() < self.coucher.timestamp() :
			self.porte = "opened"
		else:
			self.porte = "closed"
		return self

	def close(self):
		""" Fermeture de la porte via les GPIO """

		# chargement des GPIO
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
		gpio.setup(self.id.gpioUp, gpio.OUT)
		gpio.setup(self.id.gpioDown, gpio.OUT)
		gpio.setup(self.id.gpioUpCtrl, gpio.IN, pull_up_down=gpio.PUD_UP)
		gpio.setup(self.id.gpioDownCtrl,gpio.IN, pull_up_down=gpio.PUD_UP)

		# fermeture de la porte
		gpio.output(self.id.gpioDown, gpio.HIGH)
		gpio.output(self.id.gpioUp, gpio.LOW)
		ctrl = gpio.wait_for_edge(self.id.gpioDownCtrl, gpio.FALLING, timeout=self.id.lengthDown*1000)

		# si le temps est épuisé
		if ctrl is None:
			self.telegram.send("Problème sur le poulailler " + self.nom + " : il n'a pas pu se fermer" )
			print('Timeout occurred')
		# si tout se passe bien
		else:
			self.telegram.send("Fermeture du poulailler : " + self.nom)
			print("")

		gpio.cleanup()
	
	def open(self):
		""" Ouverture de la porte via les GPIO """
		
		# chargement des GPIO
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
		gpio.setup(self.id.gpioUp, gpio.OUT)
		gpio.setup(self.id.gpioDown, gpio.OUT)
		gpio.setup(self.id.gpioUpCtrl, gpio.IN, pull_up_down=gpio.PUD_UP)
		gpio.setup(self.id.gpioDownCtrl,gpio.IN, pull_up_down=gpio.PUD_UP)

		# ouverture de la porte
		gpio.output(self.id.gpioUp, gpio.HIGH)
		gpio.output(self.id.gpioDown, gpio.LOW)
		ctrl = gpio.wait_for_edge(self.id.gpioUpCtrl, gpio.FALLING, timeout=self.id.lengthUp*1000)

		# si le temps est épuisé
		if ctrl is None:
			self.telegram.send("Problème sur le poulailler " + self.nom + " : il n'a pas pu s'ouvrir" )
		# si tout se passe bien
		else:
			self.telegram.send("Ouverture du poulailler : " + self.nom)
		
		gpio.cleanup()

	def modifieState(self):
		""" Ouverture/Fermeture de la porte à l'heure du prochain évènement"""

		# On calcule le temps d'attente avant la prochain action
		liste = [self.lever, self.coucher]
		liste.sort()
		wait = int(liste[0].timestamp()) - int(datetime.now().timestamp()) 
		self.telegram.send("Prochaine action de " + self.nom + " à " + str(liste[0]))

		# on met le programe en pause
		time.sleep(wait+15)

		# statut de la porte souhaité
		self.stateDoor()

		# controle et changement si nécessaire
		if self.porte == 'opened':
			print("Ouverture de la porte")
			self.open()
		elif self.porte == 'closed':
			print("Fermeture de la porte")
			self.close()

if __name__ == '__main__':
	coq = init()
	print(coq.porte)
	print(coq.coucher)
	print(coq.lever)
	print(coq.stateDoor().porte)
