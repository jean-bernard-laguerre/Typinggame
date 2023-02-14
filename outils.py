import pygame
import random
import string

class Joueur():

    def __init__(self, x, y):
        
        self.image = pygame.image.load("images/spaceship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.bouclier_image = pygame.image.load("images/shield.png")
        self.bouclier_image = pygame.transform.scale(self.bouclier_image, (50, 50))

        self.rect = self.image.get_rect()
        self.bouclier_rect = self.bouclier_image.get_rect()
        self.rect.topleft = (x, y)

        self.vitesse = 0
        self.bouclier = False

    def affichage(self, surface):

        a ,b = surface.get_size()

        if self.rect.y + self.rect.h <= b:
            self.vitesse += .2

        if self.rect.y + self.rect.h >= b-100 and self.vitesse > 0:
            self.vitesse = 0
            self.bouclier = False

        self.rect.y += self.vitesse

        surface.blit(self.image, self.rect)

        if self.bouclier:
            self.bouclier_rect.topleft = (self.rect.x, self.rect.y)
            surface.blit(self.bouclier_image, self.bouclier_rect)

    def saut(self):
        
        self.vitesse = -4


class Obstacle():
    def __init__(self, x, y):
        
        self.image = pygame.image.load("images/obstacle.png")
        self.image = pygame.transform.scale(self.image, (250, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.mot = mot_hasard(1)
        self.descente = False
        self.palier = self.rect.y + 180

    def affichage_actif(self, surface, police, reponse):
        
        for i in range(len(self.mot)):

            try:
                if reponse[i] == self.mot[i]:
                    mot_surface = police.render(f"{self.mot[i]}", 1, 'green')
                else:
                    mot_surface = police.render(f"{self.mot[i]}", 1, 'red')

            except:
                mot_surface = police.render(f"{self.mot[i]}", 1, 'white')

            surface.blit(mot_surface, (self.rect.x+(i*17), self.rect.y - 25))
            surface.blit(self.image, self.rect)
        
        self.chute()
    
    def affichage_inactif(self, surface, police):

        for i in range(len(self.mot)):

            mot_surface = police.render(f"{self.mot[i]}", 1, 'white')

            surface.blit(mot_surface, (self.rect.x+(i*17), self.rect.y - 25))
            surface.blit(self.image, self.rect)

        self.chute()

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
        self.joueur = Joueur(300, 470)
        self.plateforme = []
        for i in range(3):
            self.plateforme += [Obstacle(200, 430-(i*180))]
        self.timer = 10
        self.index = 0
        self.score = 0
        self.vie = 3
        self.reponse = ""
        
    def affichage(self, surface, police):

        if len(self.reponse) == len(self.plateforme[0].mot) or self.timer <= 0:

            self.validation()
        
        self.joueur.affichage(surface)
        for i,element in enumerate(self.plateforme):
            if i == 0:
                element.affichage_actif(surface, police, self.reponse)
            else:
                element.affichage_inactif(surface, police)

        if self.plateforme[0].rect.y >= self.joueur.rect.y+30:
            self.plateforme.pop(0)

        score = police.render(f"Score: {self.score}", 1 ,'white')
        temps = police.render(f"{self.timer//1}", 1 ,'white')
        surface.blit(score,(25, 25))
        surface.blit(temps,(740, 25))
        self.barre(surface)

        for i in range(self.vie):
            coeur = pygame.image.load("images/life.png")
            coeur = pygame.transform.scale(coeur, (25,23))

            surface.blit(coeur, (25+(i*30), 55))

        if self.index == 10:
            jouer_son("bruitage/victory.wav")
            return True

        elif self.vie == 0:
            jouer_son("bruitage/defeat.wav")
            return True
    
    def validation(self):

        if self.reponse == self.plateforme[0].mot:
            self.index += 1
            self.score += int(len(self.plateforme[0].mot)*self.timer//1)
            self.joueur.bouclier = True
            jouer_son("bruitage/shield.wav")
            
        else:
            self.vie -= 1
            jouer_son("bruitage/digital-hit.wav")

        self.joueur.saut()
        pygame.mixer.music.play()
        self.plateforme += [Obstacle(200, -110)]

        for element in self.plateforme:
            element.descendre()

        self.reponse = ""
        self.timer = 10
    
    def barre(self, surface):

        frame = pygame.Rect(50, 100, 25, 450)
        progres = pygame.Rect(52, 550-(self.index*(450//10)), 23, self.index*(450//10))
        
        pygame.draw.rect(surface, 'aquamarine3', progres)
        pygame.draw.rect(surface, 'white', frame, 2)
        

class Bouton():
    def __init__(self, message, x, y, police, couleur):
        self.texte = police.render(message, 1, couleur)
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x, y)
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

        pygame.draw.rect(surface, 'red', self.rect, 2)
        surface.blit(self.texte, ( self.rect.x+10, self.rect.y+10))

        return action


#Recupere un mot au hasard d'un fichier defini
def mot_hasard(niveau):

    match niveau:
        case 1:
            f = open("dictionnaires/motsFacile.txt", "r")
        case 2:
            f = open("dictionnaires/motsMedium.txt", "r")
        case 3:
            f = open("dictionnaires/motsDifficile.txt", "r")
        case _:
            f = open("dictionnaires/mots.txt", "r")

    mots = f.read().splitlines()
    f.close()

    return random.choice(mots)


def jouer_son(titre):
    pygame.mixer.music.load(titre)
    pygame.mixer.music.play()