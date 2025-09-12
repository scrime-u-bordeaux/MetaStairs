# Répertoire du projet Métastairs (Métapiano + Pianostairs)

### Ce répertoire est composé de 4 sous-dossiers :

* Arduino : contient tous les scripts en C++ codés sur Arduino.
* fichiers_midi : contient tous les fichiers MIDI nécessaires au fonctionnement des scripts Python dans le dossier code.
* sons : contient tous les dossiers/fichiers .wav ou .mp3 nécessaires au fonctionnement des scripts Python dans le dossier code.
* code : contient les scripts principaux pour faire fonctionner le Métastairs.
	Pour les 2 modes suivants, il faut créer un répertoire log dans le répertoire courant. Sinon, les scripts créeront les fichiers d'enregistrement .csv dans le répertoire courant :
	pianoNormal.py : mode piano normal (à exécuter dans le terminal : python3 pianoNormal.py <nom_fichier.csv>)
  * midifileMetastairs.py : mode métapiano (à exécuter dans le terminal : python3 midifileMetastairs.py <nom_fichier.csv>)
  Pour ce mode, les fichiers .mid sont à modifier directement dans le script.
  * shepard.py : mode permettant de jouer la gamme de Shepard (à exécuter dans le terminal : python3 shepard.py)
  * modeJeuMan.py : script qui fait appel aux 3 scripts précédents et permet de passer de l’un à l’autre manuellement en appuyant sur espace.
  * modeJeuAuto.py : script qui fait appel aux 3 scripts précédents et qui les exécute automatiquement toutes les 20 minutes dans l'ordre suivant : pianoNormal, midifileMetastairs, shepard.

### Principe
Des scripts Python permettent de transformer des capteurs de pression (FSR), connectés à un microcontrôleur (ex. Teensy / Arduino), en touches de piano interactives. Chaque capteur déclenche la lecture d’un son .wav correspondant à une note précise du clavier (Do, Ré, Mi…), avec un volume dynamique basé sur la force exercée sur le capteur.
