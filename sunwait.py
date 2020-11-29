#!/usr/bin/python3
# coding: utf-8

import ephem
import re
from datetime import datetime
import time


class poulailler(object):
	"""docstring for poulailler
	- horizon (-6 pour civil, -12 nautique, -18 pour astronomique)
	- latitude (par ex 48.35)
	- longitude (par ex -1.06)
	- lever du soleil
	- coucher coucher du soleil
	"""

	def __init__(self, horizon, latitude, longitude):
		""" calcul automatiquement le prochain lever de soleil et le prochain coucher de soleil """

		
		def _listDate(date):
			""" convertir la date ephem en date datetime et rajoute le décalage horaire """
			# recupérationd des éléments de la date
			regex = re.compile("(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})")
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
			self._position = localisation
			return self._position; 

		
		def sunrise(self):
			""" lever du soleil """
			hour = self._position.next_rising(ephem.Sun())
			self.lever = _listDate(str(hour))
			return self.lever;

		
		def sunset(self):
			""" coucher du soleil """
			hour = self._position.next_setting(ephem.Sun())
			self.coucher = _listDate(str(hour))
			return self.coucher;

		self.horizon = horizon
		self.latitude = latitude
		self.longitude = longitude
		self._position = _position(self)
		self.lever = sunrise(self)
		self.coucher = sunset(self)
		



coq = poulailler('-12', '48.39', '-1.06')
print(coq.coucher)
print(coq.lever)
help(coq)
