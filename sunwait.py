#!/usr/bin/python3
# coding: utf-8

import ephem
import re
from datetime import datetime
import time
import os


class poulailler(object):
	"""docstring for poulailler
	- horizon : -6 pour civil, -12 nautique, -18 pour astronomique
	- latitude : par exemple 48.35)
	- longitude : par exemple -1.06
	- lever : horaire de lever du soleil
	- coucher : horaire de coucher du soleil
	- heure : heure actuelle
	- porte : état dans lequel la porte devrait être
	- checkState() : vérifie si la porte est dans le bon état
	- check : dernier état connu de la porte
	"""

	def __init__(self, horizon, latitude, longitude):
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
		
		def stateDoor(self):
			""" détermine si la porte est ouverte ou fermée en fonction de l'horaire """
			if self.lever.hour < self.heure.hour <self.coucher.hour:
				state = "opened"
			else:
				state = "closed"
			return state


		self.horizon = horizon
		self.latitude = latitude
		self.longitude = longitude
		self.position = _position(self)
		self.lever = sunrise(self)
		self.coucher = sunset(self)
		self.heure = datetime.now()
		self.porte = stateDoor(self)
		self.check = ''
	
	def checkState(self):
		""" vérifie si le statut de la porte correspond bien à celui qu'elle devrait avoir."""
		# statut de la porte souhaité
		statut = self.porte

		# on test si le fichier de statut existe
		if os.path.exists('statut.txt') == False:
			os.system("touch statut.txt")

		# statut de la porte réél 
		file = open("statut.txt", "r")
		saveStatut = file.readline()
		file.close()

		# controle et changement si nécessaire
		if statut != saveStatut:
			if statut == 'opened':
				self._open()
			elif statut == 'closed':
				self._close()
		
		self.check = statut
		return self
	
	"""ferme la porte"""
	def _close(self):
		file = open('statut.txt', "w")
		file.write('closed')
		file.close()
	
	"""ouvre la porte"""
	def _open(self):
		file = open('statut.txt', "w")
		file.write('opened')
		file.close()

if __name__ == '__main__':
	coq = poulailler('-6', '48.35', '-1.06')
	coq.checkState()
	print(coq.check)	