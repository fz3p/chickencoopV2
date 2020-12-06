# installation 

## Pré-requis

```
sudo apt install python3-pip RPi.GPIO git
pip3 install ephem requests

```

## cloner le dépot

```
git clone https://github.com/fz3p/chickecoopV2.git chickencoopV2
cd chickencoopV2
mv identifiant.conf.sample identifiant.conf
nano identifiant.conf
```

Editer les paramètres en fonction de votre configuration.

# Tester

dans la console python

```
> import chickenhouse
> c = chickenhouse.init()
> c.close()
```

La porte se ferme et vous recevez une notification. 

#  Automatiser

* soit à partir de l'utilisateur pi qui fait partie du groupe GPIO
* soit à partir du sudo

```
crontab -e
```

Ajouter deux lignes : 

```
0 16 * * * python3 /home/pi/chickencoopV2/poulailler.py
0 1 * * * python3 /home/pi/checkencoopV2/poulailler.py
```

pour le coucher je me suis basé sur l'horaire de coucher civil (-6°) du solstice d'hiver, 
pour le lever je me suis basé sur l'horaire de lever astronomique (-18) du solstice d'été

# Site 

https://journaldunarchiviste.fr