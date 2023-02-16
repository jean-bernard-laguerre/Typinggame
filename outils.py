import pygame
import random
import json

#Recupere un mot au hasard d'un fichier defini
def mot_hasard(langue, type):

    f = open("dictionnaires/mots.json", "r+")
    mots = json.load(f)
    f.close
    
    if langue != "Multi":
        return random.choice(mots[langue][type]) 

    liste_mots = []
    for lng in mots:
        liste_mots += mots[lng][type]

    return random.choice(liste_mots)

#Joue un son sur le canal 1
def jouer_son(titre):
    son = pygame.mixer.Sound(titre)
    pygame.mixer.Channel(1).play(son)


#Ajoute le score dans scores.json
def enregistrer(score,langue,type):

    f = open("scores.json", "r+")
    scores = json.load(f)

    if f"{langue}:{type}" not in scores:
        scores[f"{langue}:{type}"] = []

    if score > 0:
        scores[f"{langue}:{type}"].append(score)

    f.seek(0)
    json.dump(scores, f, indent=4)

    f.close()

#Recupere les dix meilleurs scores
def recuperer(langue,type):

    f = open("scores.json", "r+")
    scores = json.load(f)

    f.close()
    return sorted(scores[f"{langue}:{type}"], reverse=True)[0]