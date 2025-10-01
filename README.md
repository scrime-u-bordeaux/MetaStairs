# MetaStairs (Metapiano + Pianostairs)

A project designed for the *Nuit des Escaliers 2025* event, organized by the *Opéra de Bordeaux* in the framework of the *Journées du Patrimoine 2025* and presented to the public at the *Pôle Juridique et Judidiaire* of the University of Bordeaux.

This repository contains :
* [The MIDI controller's firmware](./Arduino) that we wrote to turn stairs into a giant MIDI controller keyboard.
* [A python program](./Python) reacting to incoming MIDI messages from the controller according to different operating modes.
* A Reaper project receiving the MIDI messages processed by the python script and playing the notes with various VST plugins according to the current operating mode.

