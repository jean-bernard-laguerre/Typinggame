import pygame
from outils import *

class Joueur():

    def __init__(self, x, y):
        
        self.image = pygame.image.load("images/spaceship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.bouclier_image = pygame.image.load("images/shield.png")
        self.bouclier_image = pygame.transform.scale(self.bouclier_image, (50, 50))

        self.rect = self.image.get_rect()
        self.bouclier_rect = self.bouclier_image.get_rect()
        self.rect.topleft = (x, y)

        self.bouclier = False
        #Vitesse de mouvement
        self.vitesse = 0

    def affichage(self, surface):

        a ,b = surface.get_size()

        #Deplace le joueur vers le bas
        if self.rect.y + self.rect.h <= b:
            self.vitesse += .2

        #Stop le joueur
        if self.rect.y + self.rect.h >= b-60 and self.vitesse > 0:
            self.vitesse = 0
            self.bouclier = False

        self.rect.y += self.vitesse

        surface.blit(self.image, self.rect)

        #Affiche le bouclier si actif
        if self.bouclier:
            self.bouclier_rect.topleft = (self.rect.x, self.rect.y)
            surface.blit(self.bouclier_image, self.bouclier_rect)

    def saut(self):
        #Deplace le joueur vers le haut
        self.vitesse = -4


class Obstacle():
    def __init__(self, x, y, type, langue):
        
        self.image = pygame.image.load("images/obstacle.png")
        self.image = pygame.transform.scale(self.image, (250, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.descente = False
        self.palier = self.rect.y + 180
        self.mot = mot_hasard(langue, type)

    def affichage_actif(self, surface, police, reponse):
        
        #Affiche le mot au dessus de l'obstacle
        for i in range(len(self.mot)):

            #Lettre verte si correcte, rouge en cas d'erreur
            try:
                if reponse[i] == self.mot[i]:
                    mot_surface = police.render(f"{self.mot[i]}", 1, 'green')
                else:
                    mot_surface = police.render(f"{self.mot[i]}", 1, 'red')

            #Lettre blanche si elle n'a pas été entrée
            except:
                mot_surface = police.render(f"{self.mot[i]}", 1, 'white')

            surface.blit(mot_surface, (self.rect.x+(i*18), self.rect.y - 25))
            surface.blit(self.image, self.rect)
        
        self.chute()
    
    def affichage_inactif(self, surface, police):

        #Affiche le mot en blanc
        for i in range(len(self.mot)):

            mot_surface = police.render(f"{self.mot[i]}", 1, 'white')

            surface.blit(mot_surface, (self.rect.x+(i*18), self.rect.y - 25))
            surface.blit(self.image, self.rect)

        self.chute()

    #Deplace l'obstacle vers le bas
    def chute(self):
        if self.descente:

            if self.rect.y < self.palier:
                self.rect.y += 5
            else:
                self.descendre()
        else:
            self.palier = self.rect.y + 180 
    
    def descendre(self):

        if self.descente:
            self.descente = False
        else:
            self.descente = True


class Jeu():
    def __init__(self) -> None:

        self.diff = 'medium'
        self.langue = 'Francais'
        self.type_mot = 'moyen'
        self.joueur = Joueur(300, 500)
        self.obstacle = []
        self.timer = self.chrono()
        self.index = 0
        self.score = 0
        self.vie = 3
        self.reponse = ""
        
    def affichage(self, surface, police):

        #Teste la reponse si le timer est a 0 ou si la reponse et le mot on la meme longueur
        if len(self.reponse) == len(self.obstacle[0].mot) or self.timer <= 0:

            self.validation()
        
        #Affiche obstacle
        self.joueur.affichage(surface)
        for i,element in enumerate(self.obstacle):
            if i == 0:
                element.affichage_actif(surface, police, self.reponse)
            else:
                element.affichage_inactif(surface, police)

        #Supprime obstacle lorsqu'il est sous le joueur
        if self.obstacle[0].rect.y >= self.joueur.rect.y+30:
            self.obstacle.pop(0)

        #Affiche score, timer, niveau et barre de progres
        score = police.render(f"Score: {self.score}", 1 ,'white')
        temps = police.render(f"{self.timer//1}", 1 ,'white')
        lbl_partie = police.render(f"{self.langue} | {self.type_mot} | {self.diff}", 1 ,'white')
        surface.blit(score,(25, 25))
        surface.blit(temps,(740, 25))
        surface.blit(lbl_partie, (475, 565))
        self.barre(surface)

        #Affiche point de vie
        for i in range(self.vie):
            coeur = pygame.image.load("images/life.png")
            coeur = pygame.transform.scale(coeur, (25,23))

            surface.blit(coeur, (25+(i*30), 55))

        #Condition de fin de partie
        if self.index == 10:
            jouer_son("bruitage/victory.wav")
            return True

        elif self.vie == 0:
            jouer_son("bruitage/defeat.wav")
            return True
    
    #Verifie si le mot a été entré correctement 
    def validation(self):

        #Ajoute des points et progresse la partie si la reponse est correcte
        if self.reponse == self.obstacle[0].mot:
            self.index += 1
            self.score += int(len(self.obstacle[0].mot)*(( self.timer / self.chrono() )*10))
            self.joueur.bouclier = True
            self.joueur.saut()
            jouer_son("bruitage/shield.wav")

        #Perd une vie sinon
        else:
            self.vie -= 1
            jouer_son("bruitage/digital-hit.wav")
        
        #Ajoute un nouvelle obstacle
        self.obstacle += [Obstacle(200, -110, self.type_mot, self.langue)]

        for element in self.obstacle:
            element.descendre()

        #Reset le timer et la reponse
        self.reponse = ""
        self.timer = self.chrono() 
    
    #Barre de progression
    def barre(self, surface):

        frame = pygame.Rect(50, 100, 25, 450)
        progres = pygame.Rect(52, 550-(self.index*(450//10)), 23, self.index*(450//10))
        
        pygame.draw.rect(surface, 'aquamarine3', progres)
        pygame.draw.rect(surface, 'white', frame, 2)

    #Temps de reponse
    def chrono(self):

        match self.diff:
            case 'facile':
                return 10
            case 'medium':
                return 7
            case 'difficile':
                return 4
        

class Bouton():
    def __init__(self, message, x, y, police, couleur):
        self.texte = police.render(message, 1, couleur)
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x-self.rect.w/2, y)
        self.rect.w = self.texte.get_width()+20
        self.rect.h = self.texte.get_height()+20

    #Affiche le bouton retourne True lorsque l'on clique a l'interieur
    def affichage(self, surface):
        
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if (pygame.mouse.get_pressed()[0] == 1):
                jouer_son("bruitage/select.wav")
                action = True

        surface.blit(self.texte, ( self.rect.x, self.rect.y))

        return action