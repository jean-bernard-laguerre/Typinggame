import pygame
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
tdr = pygame.time.Clock()
tps = 0
police = pygame.font.SysFont('Verdana', 16)
police_jeu = pygame.font.SysFont('courier', 24)

statut_partie = 0

def ecran_menu():

    global statut_partie

    if Bouton("Jouer", 350, 350, police).affichage(fenetre):
        nouvelle_partie()
        statut_partie = 1

def ecran_jeu():
    global statut_partie

    if jeu.affichage(fenetre, police_jeu):
        statut_partie = 2

def ecran_fin():
    global statut_partie
    
    score = police.render(f"Score: {jeu.score} points", 1 ,'black')

    if jeu.vie == 0:
        resultat = police.render("Defaite", 1 ,'black')
    else:
        resultat = police.render("Victoire", 1 ,'black')
        fenetre.blit(score, (350, 320))
        
    fenetre.blit(resultat, (350, 295))
    
    if Bouton("Retour Menu", 600, 500, police).affichage(fenetre):

        statut_partie = 0

def nouvelle_partie():
    global jeu

    jeu = Jeu()


en_cours = True
while en_cours:

    tps = tdr.tick(60) / 1000
    fenetre.fill((255,255,255))

    match statut_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
            jeu.timer -= tps
        case 2:
            ecran_fin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
            
        if event.type == pygame.KEYDOWN and statut_partie == 1:
            if event.key == pygame.K_BACKSPACE:
                jeu.reponse = jeu.reponse[:-1]

            elif pygame.key.name(event.key) in string.ascii_lowercase:
                jeu.reponse += pygame.key.name(event.key)
    
    pygame.display.update()

pygame.quit()