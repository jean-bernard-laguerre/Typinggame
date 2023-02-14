import pygame
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
pygame.display.set_caption("Typing Game")
tdr = pygame.time.Clock()
tps = 0
police = pygame.font.Font('polices\Orbitron-Medium.ttf', 32)
police_jeu = pygame.font.Font('polices\ChargeVectorBold.ttf', 24)

bg_menu = pygame.image.load("images/bg_menu.png")
bg_menu_rect = bg_menu.get_rect()

bg_jeu = pygame.image.load("images/bg_jeu.png")
bg_jeu_rect = bg_jeu.get_rect()

bg_victoire = pygame.image.load("images/bg_victory.png")
bg_victoire_rect = bg_jeu.get_rect()

bg_defaite = pygame.image.load("images/bg_defeat.png")
bg_defaite_rect = bg_jeu.get_rect()

statut_partie = 0

def ecran_menu():

    global statut_partie

    fenetre.blit(bg_menu, bg_menu_rect)

    if Bouton("JOUER", 320, 350, police, 'white').affichage(fenetre):
        nouvelle_partie()
        statut_partie = 1

def ecran_jeu():
    global statut_partie

    fenetre.blit(bg_jeu, bg_jeu_rect)

    if jeu.affichage(fenetre, police_jeu):
        statut_partie = 2

def ecran_fin():
    global statut_partie
    
    score = police.render(f"Score: {jeu.score} points", 1 ,'white')

    if jeu.vie == 0:
        fenetre.blit(bg_defaite, bg_defaite_rect)
        resultat = police.render("Defaite", 1 ,'black')
    else:
        fenetre.blit(bg_victoire, bg_victoire_rect)
        resultat = police.render("Victoire", 1 ,'white')
        fenetre.blit(score, (250, 320))
    
    
    fenetre.blit(resultat, (325, 295))
    
    if Bouton("Retour Menu", 500, 500, police, 'white').affichage(fenetre):

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