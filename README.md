# MetaStairs (Metapiano + Pianostairs)

Un projet réalisé pour la Nuit des Escaliers 2025 (un évènement organisé par l'Opéra de Bordeaux dans le cadre des Journées du Patrimoine 2025) et présenté au Pôle Juridique et Judiciaire de l'Université de Bordeaux place Pey-Berland

Ce dépôt contient :
* [Le firmware du contrôleur MIDI](./Arduino) utilisé pour rendre l'escalier interactif.
* [Un script python](./code) réagissant aux messages MIDI reçus du contrôleur selon différents modes de jeu.
* Un projet reaper recevant les messages MIDI traités par le script python et générant des sons en fonction du mode de jeu actif.

