import pygame
import random
import string

class Joueur():

    def __init__(self, x, y):
        
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vitesse = 0

    def affichage(self, surface):

        a ,b = surface.get_size()

        if self.rect.y + self.rect.h <= b:
            self.vitesse += .2

        if self.rect.y + self.rect.h >= b-100 and self.vitesse > 0:
            self.vitesse = 0

        self.rect.y += self.vitesse

        pygame.draw.rect(surface, 'darkgreen', self.rect)

    def saut(self):
        
        self.vitesse = -4


class Obstacle():

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 75, 75)

    def affichage(self, surface):

        pygame.draw.rect(surface, 'blue', self.rect)


class Plateforme():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 10)
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
                mot_surface = police.render(f"{self.mot[i]}", 1, 'black')

            surface.blit(mot_surface, (self.rect.x+(i*12), self.rect.y - 25))
            pygame.draw.rect(surface, 'darkblue', self.rect)
        
        self.chute()
    
    def affichage_inactif(self, surface, police):

        for i in range(len(self.mot)):

            mot_surface = police.render(f"{self.mot[i]}", 1, 'black')

            surface.blit(mot_surface, (self.rect.x+(i*12), self.rect.y - 25))
            pygame.draw.rect(surface, 'darkblue', self.rect)

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
            self.plateforme += [Plateforme(200, 500-(i*180))]
        self.timer = 10
        self.index = 0
        self.score = 0
        self.vie = 3
        self.reponse = ""
        
    def affichage(self, surface, police):

        if len(self.reponse) == len(self.plateforme[0].mot) or self.timer < 0:

            self.validation()
        
        self.joueur.affichage(surface)
        for i,element in enumerate(self.plateforme):
            if i == 0:
                element.affichage_actif(surface, police, self.reponse)
            else:
                element.affichage_inactif(surface, police)

        score = police.render(f"Score: {self.score}", 1 ,'black')
        temps = police.render(f"{self.timer//1}", 1 ,'black')
        surface.blit(score,(25, 25))
        surface.blit(temps,(740, 25))
        self.barre(surface)

        for i in range(self.vie):
            pygame.draw.rect(surface, 'red', pygame.Rect(25+(i*30), 50, 25, 25))

        if self.index == 20:
            return True
        elif self.vie == 0:
            return True
    
    def validation(self):

        if self.reponse == self.plateforme[0].mot:
            self.index += 1
            self.score += int(len(self.plateforme[0].mot)*self.timer//1)
        else:
            self.vie -= 1

        self.joueur.saut()
        self.plateforme.pop(0)
        self.plateforme += [Plateforme(200, -40)]
        for element in self.plateforme:
            element.descendre()

        self.reponse = ""
        self.timer = 10
    
    def barre(self, surface):

        frame = pygame.Rect(50, 100, 25, 450)
        progres = pygame.Rect(52, 548-(self.index*(448//20)), 21, self.index*(447//20))

        pygame.draw.rect(surface, 'black', frame, 2)
        pygame.draw.rect(surface, 'red', progres)


class Bouton():
    def __init__(self, message, x, y, police):
        self.texte = police.render(message, 1, 'black')
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