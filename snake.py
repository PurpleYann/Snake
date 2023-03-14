# =-=-=-=-=-=-=-= Snake v1.4 =-=-=-=-=-=-=-=
#
# Crée par : Yann & Emmanuel
#
# Dernier Ajout : Récupération des Points.
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#         Initialisation du Projet :
#          Importation des Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import pygame
import time
import random

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#  Etape 0 : Création de la classe Score
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Score:
    # Classe de gestion du score.
    def __init__(self,score,meilleurscore):
        self.score = score
        self.mscore = meilleurscore
        
    def affscore(self):
        '''
        Variable du score (Utilisée pour les affichages & autre)
        '''
        return self.score
    
    def affmscore(self):
        '''
        Variable du meilleur score (Utilisée pour les affichages & autre)
        '''
        return self.mscore
    
    def scores(self):
        '''
        Renvoie les scores. Ce message s'envoie lorsque vous mourrez.
        '''
        print("[Snake] Dernier score ajouté: " + str(self.score) + "\nMeilleur score: " + str(self.mscore))
    
    def afficherscore(self):
        '''
        Renvoie le dernier score ajouté. Utilisation manuelle nécessaire.
        '''
        print("[Snake] Dernier score ajouté: " + str(self.score))
        
    def affmeilleurscore(self):
        '''
        Renvoie le meilleur score actuel. Utilisation manuelle nécessaire.
        '''
        print("[Snake] Meilleur score: " + str(self.mscore))
        
    def meilleurscore(self,nvscore):
        '''
        Vérification du score en cas de nouveau record.
        S'effectue automatiquement quand vous mourrez.
        '''
        if self.mscore < nvscore:
            print("[Snake] Nouveau Record ! "+str(self.score))
            self.mscore = nvscore
        
    def ajouterscore(self,nvscore):
        '''
        Permet d'ajouter des scores à la main.
        Utilisé à des fins de test.
        '''
        self.score = nvscore
        self.meilleurscore(nvscore)
        
    def recupererscores(self):
        '''
        Permet de récupérer les scores.
        '''
        
        # Récupère depuis 'score.txt'.
        fichierscore = open("score.txt", "r")
        anciencompteur = fichierscore.readline()
        fichierscore.close()

        # Assigne le dernier score.
        self.score = int(anciencompteur)

        # Récupère depuis 'mscore.txt'.
        fichiermscore = open("mscore.txt", "r")
        anciensompteur2 = fichiermscore.readline()
        fichiermscore.close()

        # Assigne le dernier meilleur score.
        self.mscore = int(anciensompteur2)
        
        #Confirmation de la tâche.
        print("[Snake] Scores actualisés avec succès !")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Etape 1 : Création de la variable
# contenant le score provenant de
# 'score.txt' & 'mscore.txt'.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Création de la variable contenant un score prédéfini (valeurs temporaires).
mon_score = Score(0,0)
# Récupération du score provenant des fichiers textes.
mon_score.recupererscores()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Etape 2 : Ecriture des scores sur les
# fichiers 'score.txt' & 'mscore.txt'.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def ecriture_fichiers():
    '''
    Permet l'écriture des scores dans les fichiers correspondants.
    - S'effectue en fin de partie.
    '''
    
    # Récupération des derniers scores.
    exp_score = mon_score.affscore()
    exp_mscore = mon_score.affmscore()
    
    # Ecriture du score dans 'score.txt'.
    fichierscore = open("score.txt","w")
    fichierscore.write(str(exp_score))
    fichierscore.close()
    
    # Ecriture du meilleur score dans 'mscore.txt'.
    fichiermscore = open("mscore.txt","w")
    fichiermscore.write(str(exp_mscore))
    fichiermscore.close()
    
    # Confirmation des actions précédentes.
    print("[Snake] Scores actualisés avec succès !")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Etape 3 : Création de l'interface PyGame
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Nécessaire à pygame.
pygame.init()

# Importation des Couleurs.
# Texte.
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
orange = (255, 187, 0)

# Snake.
green = (0, 255, 0)
# Arrière Plan.
blue = (50, 153, 213)

# Ajustement de l'interface.

dis_width = 600
dis_height = 400

# Création de la fenêtre et de son titre.

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake v1.4 | By Yann & Emmanuel')

# Clock nécessaire pour la limite de FPS & la vitesse du Snake.
clock = pygame.time.Clock()

# Configuration du Snake.
snake_block = 10
snake_speed = 15

# Paramères liés au texte.
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("arial", 35)

# Création du score.

def Your_score():
    '''
    Renvoie le texte lié au score (En Haut à Gauche).
    Présent durant toute la partie.
    '''
    value = score_font.render("Your Score: " + str(mon_score.affscore()), True, yellow)
    dis.blit(value, [0, 0])

def MeilleurScore():
    '''
    Renvoie le texte lié au meilleur score (En Haut à Gauche, en dessous du Score).
    Présent durant toute la partie.
    '''
    value = score_font.render("H-Score: " + str(mon_score.affmscore()), True, orange)
    dis.blit(value, [0,25])    

# Création du serpent

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Création du message de fin.

def message(msg, color):
    '''
    Permet la création des messages de fin.
    Présent lors de la mort du snake.
    '''
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
# Création du gameplay.

def gameLoop():
    '''
    Commande finale.
    Regroupe toutes les variables/définitions/classes utilisées au dessus.
    Contient certaines classes nécessaires au jeu ainsi que le jeu en lui même.
    '''
    # Variables de contrôle du jeu.
    game_over = False
    game_close = False
    affmeilleurscore = None

    # Spawn du snake.
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    
    # Configuration de base du Snake.
    # Signifie un snake de taille 1 (tête) avec une queue de taille 0 (sans queue).
    snake_List = []
    Length_of_snake = 1
 
    # Localisation de la nourriture.
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Détection de la mort.
    while not game_over:
 
        # Détection Unique. S'effectue une fois.
        if game_close == True:
            mon_score.scores()
            mon_score.ajouterscore(mon_score.affscore())
            ecriture_fichiers()

        # Détection Indéfinie. S'effectue jusqu'au nouveau lancement de la partie.
        while game_close == True:
            dis.fill(blue)
            Your_score()
            MeilleurScore()
            
            if affmeilleurscore == False:
                # Affichage Basique.
                message("Perdu! R:Rejouer | Q:Quitter", black)
            else:
                # Affichage lors d'un meilleur score.
                message("Meilleur Score ! R:Rejouer | Q:Quitter", red)
            pygame.display.update()
 
            # Détection des touches lors de la mort.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()
        
        # Détection des touches en jeu.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        # Variable nécessaire à la détection de la mort par les murs.
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        
        # Variables nécessaire au déplacement du snake.
        x1 += x1_change
        y1 += y1_change
        
        # Couleur de fond.
        dis.fill(blue)
        
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        
        Your_score()
        
        mon_score.ajouterscore(Length_of_snake - 1)
 
        if int(mon_score.score) >= int(mon_score.mscore):
            affmeilleurscore = True
        else:
            affmeilleurscore = False
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()

gameLoop()