import pygame
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
pygame.display.set_caption("Typing Game")
tdr = pygame.time.Clock()
tps = 0
police_menu = pygame.font.Font('polices\Orbitron-Medium.ttf', 32)
police_menu_gras = pygame.font.Font('polices\Orbitron-ExtraBold.ttf', 32)
police_jeu = pygame.font.Font('polices\ChargeVectorBold.ttf', 24)
couleur_inactif = 'darkred'
couleur_actif = 'red'

bg_menu = pygame.image.load("images/bg_menu.png")
bg_menu_rect = bg_menu.get_rect()

bg_jeu = pygame.image.load("images/bg_jeu.png")
bg_jeu_rect = bg_jeu.get_rect()

bg_victoire = pygame.image.load("images/bg_victory.png")
bg_victoire_rect = bg_jeu.get_rect()

bg_defaite = pygame.image.load("images/bg_defeat.png")
bg_defaite_rect = bg_jeu.get_rect()

jeu = Jeu()
statut_partie = 0

def ecran_menu():

    fenetre.blit(bg_menu, bg_menu_rect)

    lbl_diff = police_menu_gras.render(f"Difficulté", 1 ,'white')
    lbl_type_mot = police_menu_gras.render(f"Mots", 1 ,'white')
    lbl_langue = police_menu_gras.render(f"Langue", 1 ,'white')
    fenetre.blit(lbl_diff, (400-(lbl_diff.get_rect().w/2), 90))
    fenetre.blit(lbl_type_mot, (400-(lbl_type_mot.get_rect().w/2), 215))
    fenetre.blit(lbl_langue, (400-(lbl_langue.get_rect().w/2), 340))

    #Difficulté temps
    if jeu.diff != 'facile':
        if Bouton("Facile", 130, 125, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'facile'
    else:
        Bouton("Facile", 130, 125, police_menu, couleur_actif).affichage(fenetre)

    if jeu.diff != 'moyen':
        if Bouton("Moyen", 330, 125, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'moyen'
    else:
        Bouton("Moyen", 330, 125, police_menu, couleur_actif).affichage(fenetre)

    if jeu.diff != 'difficile':
        if Bouton("Difficile", 530, 125, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'difficile'
    else:
        Bouton("Difficile", 530, 125, police_menu, couleur_actif).affichage(fenetre)

    #Longueur mots
    if jeu.type_mot != 'court':
        if Bouton("Court", 130, 250, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'court'
    else:
        Bouton("Court", 130, 250, police_menu, couleur_actif).affichage(fenetre)

    if jeu.type_mot != 'moyen':
        if Bouton("Moyen", 330, 250, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'moyen'
    else:
        Bouton("Moyen", 330, 250, police_menu, couleur_actif).affichage(fenetre)

    if jeu.type_mot != 'long':
        if Bouton("Long", 530, 250, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'long'
    else:
        Bouton("Long", 530, 250, police_menu, couleur_actif).affichage(fenetre)

    #Langue mots
    if jeu.langue != 'Francais':
        if Bouton("Francais", 130, 375, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Francais'
    else:
        Bouton("Francais", 130, 375, police_menu, couleur_actif).affichage(fenetre)

    if jeu.langue != 'Anglais':
        if Bouton("Anglais", 330, 375, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Anglais'
    else:
        Bouton("Anglais", 330, 375, police_menu, couleur_actif).affichage(fenetre)

    if jeu.langue != 'Multi':
        if Bouton("Multi", 530, 375, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Multi'
    else:
        Bouton("Multi", 530, 375, police_menu, couleur_actif).affichage(fenetre)
            
    #Bouton demarrage
    if Bouton("JOUER", 320, 500, police_menu, 'white').affichage(fenetre):
        jeu.timer = jeu.chrono()
        for i in range(3):
            jeu.obstacle += [Obstacle(200, 430-(i*180), jeu.type_mot, jeu.langue)]
        navigation(1)


def ecran_jeu():

    fenetre.blit(bg_jeu, bg_jeu_rect)

    if jeu.affichage(fenetre, police_jeu):
        navigation(2)


def ecran_fin():

    score = police_menu.render(f"Score: {jeu.score} points", 1 ,'white')

    if jeu.vie == 0:
        fenetre.blit(bg_defaite, bg_defaite_rect)
        resultat = police_menu.render("Defaite", 1 ,'black')
    else:
        fenetre.blit(bg_victoire, bg_victoire_rect)
        resultat = police_menu.render("Victoire", 1 ,'white')
        fenetre.blit(score, (250, 320))
    
    
    fenetre.blit(resultat, (325, 295))
    
    if Bouton("Retour Menu", 500, 500, police_menu, 'white').affichage(fenetre):
        navigation(0)
        nouvelle_partie()


def nouvelle_partie():
    global jeu

    jeu = Jeu()

def navigation(page):
    global statut_partie
    statut_partie = page


#Boucle principale
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