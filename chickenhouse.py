#!/usr/bin/python3
# coding: utf-8

import ephem
import re
from datetime import datetime
import time
import os
import login


class init(object):
	"""docstring for chickenhouse
	- horizon : -6 pour civil, -12 nautique, -18 pour astronomique
	- latitude : par exemple 48.35)
	- longitude : par exemple -1.06
	- lever : horaire de lever du soleil
	- coucher : horaire de coucher du soleil
	- heure : heure actuelle
	- porte : état dans lequel la porte devrait être
	- nom : nom du poulailler
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
			localisation.horizon, localisation.lat, localisation.long = self.horizon, self.latitude, self.longitude
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
		
		def gpio():
			gpio.setmode(gpio.BCM)
			gpio.setwarnings(False)
			gpio.setup(id.gpioUp, gpio.OUT)
			gpio.setup(id.gpioDown, gpio.OUT)
		
		id = login.init()

		self.horizon = id.horizon
		self.latitude = id.latitude
		self.longitude = id.longitude
		self.position = _position(self)
		self.lever = sunrise(self)
		self.coucher = sunset(self)
		self.heure = datetime.now()
		self.porte = ''
		self.nom = id.name
	

	def stateDoor(self):
		""" détermine si la porte est ouverte ou fermée en fonction de l'horaire """
		if self.lever.timestamp() < datetime.now().timestamp() < self.coucher.timestamp() :
			self.porte = "opened"
		else:
			self.porte = "closed"
		return self

	def close(self):
		gpio.output(id.gpioDown, gpio.HIGH)
		gpio.output(id.gpioUp, gpio.LOW)
		time.sleep(45)
		pass
	
	def open(self):
		gpio.output(id.gpioUp, gpio.HIGH)
		gpio.output(id.gpioDown, gpio.LOW)
		time.sleep(45)
		pass

if __name__ == '__main__':
	coq = init()
	print(coq.porte)
	print(coq.coucher)
	print(coq.lever)
	print(coq.stateDoor().porte)
