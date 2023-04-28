import pygame
import string
from outils import *
from classes import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
pygame.display.set_caption("Typing Game")

tdr = pygame.time.Clock()
tps = 0


#Polices, images, musique
police_menu = pygame.font.Font('polices\Orbitron-Medium.ttf', 32)
police_menu_gras = pygame.font.Font('polices\Orbitron-ExtraBold.ttf', 32)
police_jeu = pygame.font.Font('polices\ChargeVectorBold.ttf', 24)
police_jeu_mid = pygame.font.Font('polices\ChargeVectorBold.ttf', 32)
police_jeu_grand = pygame.font.Font('polices\ChargeVectorBold.ttf', 48)

couleur_inactif = 'grey70'
couleur_actif = 'red'

bg_menu = pygame.image.load("images/bg_menu.png")
bg_menu_rect = bg_menu.get_rect()

bg_menu_frame = pygame.image.load("images/bg_menu_frame.png")
bg_menu_frame_rect = bg_menu.get_rect()

bg_menu_frame_mini = pygame.image.load("images/bg_menu_frame_mini.png")
bg_menu_frame_mini_rect = bg_menu.get_rect()

bg_jeu = pygame.image.load("images/bg_jeu.png")
bg_jeu_rect = bg_jeu.get_rect()

bg_victoire = pygame.image.load("images/bg_victory.png")
bg_victoire_rect = bg_jeu.get_rect()

bg_defaite = pygame.image.load("images/bg_defeat.png")
bg_defaite_rect = bg_jeu.get_rect()

pygame.mixer.music.load("musique/Audiorezout - Subterranean.mp3")



jeu = Jeu()
statut = 0
pygame.mixer.music.set_volume(.7)
pygame.mixer.music.play(-1)



#Menu Principal
def ecran_menu():

    fenetre.blit(bg_menu, bg_menu_rect)
    fenetre.blit(bg_menu_frame, bg_menu_frame_rect)

    lbl_diff = police_menu_gras.render(f"Difficulté", 1 ,'white')
    lbl_type_mot = police_menu_gras.render(f"Mots", 1 ,'white')
    lbl_langue = police_menu_gras.render(f"Langue", 1 ,'white')
    fenetre.blit(lbl_diff, (400-(lbl_diff.get_rect().w/2), 100))
    fenetre.blit(lbl_type_mot, (400-(lbl_type_mot.get_rect().w/2), 225))
    fenetre.blit(lbl_langue, (400-(lbl_langue.get_rect().w/2), 350))

    #Difficulté temps
    if jeu.diff != 'facile':
        if Bouton("Facile", 150, 145, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'facile'
    else:
        Bouton("Facile", 150, 145, police_menu, couleur_actif).affichage(fenetre)

    if jeu.diff != 'medium':
        if Bouton("Medium", 400, 145, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'medium'
    else:
        Bouton("Medium", 400, 145, police_menu, couleur_actif).affichage(fenetre)

    if jeu.diff != 'difficile':
        if Bouton("Difficile", 650, 145, police_menu, couleur_inactif).affichage(fenetre):
            jeu.diff = 'difficile'
    else:
        Bouton("Difficile", 650, 145, police_menu, couleur_actif).affichage(fenetre)

    #Longueur mots
    if jeu.type_mot != 'court':
        if Bouton("Court", 150, 270, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'court'
    else:
        Bouton("Court", 150, 270, police_menu, couleur_actif).affichage(fenetre)

    if jeu.type_mot != 'moyen':
        if Bouton("Moyen", 400, 270, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'moyen'
    else:
        Bouton("Moyen", 400, 270, police_menu, couleur_actif).affichage(fenetre)

    if jeu.type_mot != 'long':
        if Bouton("Long", 650, 270, police_menu, couleur_inactif).affichage(fenetre):
            jeu.type_mot = 'long'
    else:
        Bouton("Long", 650, 270, police_menu, couleur_actif).affichage(fenetre)

    #Langue mots
    if jeu.langue != 'Francais':
        if Bouton("Francais", 150, 395, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Francais'
    else:
        Bouton("Francais", 150, 395, police_menu, couleur_actif).affichage(fenetre)

    if jeu.langue != 'Anglais':
        if Bouton("Anglais", 400, 395, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Anglais'
    else:
        Bouton("Anglais", 400, 395, police_menu, couleur_actif).affichage(fenetre)

    if jeu.langue != 'Multi':
        if Bouton("Multi", 650, 395, police_menu, couleur_inactif).affichage(fenetre):
            jeu.langue = 'Multi'
    else:
        Bouton("Multi", 650, 395, police_menu, couleur_actif).affichage(fenetre)
            
    #Bouton demarrage
    if Bouton("JOUER", 400, 500, police_jeu_grand, 'white').affichage(fenetre):
        jeu.timer = jeu.chrono()
        for i in range(3):
            jeu.obstacle += [Obstacle(200, 430-(i*180), jeu.type_mot, jeu.langue)]
        navigation(1)



def ecran_jeu():

    fenetre.blit(bg_jeu, bg_jeu_rect)

    if jeu.affichage(fenetre, police_jeu):
        if jeu.vie > 0:
            enregistrer(jeu.score, jeu.langue, jeu.type_mot)
        navigation(2)



def ecran_fin():

    score = police_menu.render(f"Score: {jeu.score} points", 1 ,'white')
    meilleur_score = police_menu.render(f"PB: {recuperer(jeu.langue, jeu.type_mot)} points", 1 ,'white')
    lbl_partie = police_jeu.render(f"{jeu.langue} | {jeu.type_mot} | {jeu.diff}", 1 ,'white')

    if jeu.vie == 0:
        fenetre.blit(bg_defaite, bg_defaite_rect)
        fenetre.blit(bg_menu_frame_mini, (200, 150))
        resultat = police_menu_gras.render("Defaite", 1 ,'white')
    else:
        fenetre.blit(bg_victoire, bg_victoire_rect)
        resultat = police_menu_gras.render("Victoire!", 1 ,'white')
        fenetre.blit(bg_menu_frame_mini, (200, 150))
        fenetre.blit(score, (400-score.get_rect().w/2, 290))
    
    fenetre.blit(lbl_partie, (400-lbl_partie.get_rect().w/2, 200))
    fenetre.blit(resultat, (400-resultat.get_rect().w/2, 250))
    fenetre.blit(meilleur_score, (400-meilleur_score.get_rect().w/2, 330))
    
    if Bouton("Retour Menu", 650, 500, police_menu, 'white').affichage(fenetre):
        navigation(0)
        nouvelle_partie()



def nouvelle_partie():
    global jeu
    jeu = Jeu()



def navigation(page):
    global statut
    statut = page




#Boucle principale
en_cours = True
while en_cours:

    tps = tdr.tick(30) / 10000
    fenetre.fill((255,255,255))

    match statut:
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
            
        if event.type == pygame.KEYDOWN and statut == 1:
            if event.key == pygame.K_BACKSPACE:
                jeu.reponse = jeu.reponse[:-1]

            elif pygame.key.name(event.key) in string.ascii_lowercase:
                jeu.reponse += pygame.key.name(event.key)
    
    pygame.display.update()

pygame.quit()