import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 640
HAUTEUR = 480
TAILLE_CELLULE = 20
LIGNES = HAUTEUR // TAILLE_CELLULE
COLONNES = LARGEUR // TAILLE_CELLULE
FPS = 10

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)

# Directions
HAUT = (0, -1)
BAS = (0, 1)
GAUCHE = (-1, 0)
DROITE = (1, 0)


class Snake:
    def __init__(self):
        self.positions = [(COLONNES // 2, LIGNES // 2)]
        self.direction = DROITE
        self.grandir = False
        
    def bouger(self):
        tete = self.positions[0]
        nouvelle_tete = (tete[0] + self.direction[0], tete[1] + self.direction[1])
        
        # Vérifier les bordures
        if (nouvelle_tete[0] < 0 or nouvelle_tete[0] >= COLONNES or
            nouvelle_tete[1] < 0 or nouvelle_tete[1] >= LIGNES):
            return False
            
        # Vérifier collision avec soi-même
        if nouvelle_tete in self.positions:
            return False
            
        self.positions.insert(0, nouvelle_tete)
        
        if not self.grandir:
            self.positions.pop()
        else:
            self.grandir = False
            
        return True
    
    def changer_direction(self, nouvelle_direction):
        # Empêcher de faire demi-tour
        if (self.direction[0] * -1, self.direction[1] * -1) != nouvelle_direction:
            self.direction = nouvelle_direction
    
    def manger(self):
        self.grandir = True
        
    def dessiner(self, ecran):
        for i, position in enumerate(self.positions):
            x = position[0] * TAILLE_CELLULE
            y = position[1] * TAILLE_CELLULE
            couleur = VERT if i == 0 else BLEU
            pygame.draw.rect(ecran, couleur, (x, y, TAILLE_CELLULE, TAILLE_CELLULE))


class Nourriture:
    def __init__(self):
        self.position = None
        self.generer()
        
    def generer(self):
        self.position = (random.randint(0, COLONNES - 1), 
                        random.randint(0, LIGNES - 1))
    
    def dessiner(self, ecran):
        x = self.position[0] * TAILLE_CELLULE
        y = self.position[1] * TAILLE_CELLULE
        pygame.draw.rect(ecran, ROUGE, (x, y, TAILLE_CELLULE, TAILLE_CELLULE))


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Snake")
        self.horloge = pygame.time.Clock()
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            elif evenement.type == pygame.KEYDOWN:
                if self.game_over:
                    if evenement.key == pygame.K_SPACE:
                        self.__init__()
                elif evenement.key == pygame.K_UP:
                    self.snake.changer_direction(HAUT)
                elif evenement.key == pygame.K_DOWN:
                    self.snake.changer_direction(BAS)
                elif evenement.key == pygame.K_LEFT:
                    self.snake.changer_direction(GAUCHE)
                elif evenement.key == pygame.K_RIGHT:
                    self.snake.changer_direction(DROITE)
        return True
    
    def mettre_a_jour(self):
        if not self.game_over:
            if not self.snake.bouger():
                self.game_over = True
                return
                
            # Vérifier si le serpent mange la nourriture
            if self.snake.positions[0] == self.nourriture.position:
                self.snake.manger()
                self.score += 10
                # Générer nouvelle nourriture qui n'est pas sur le serpent
                while self.nourriture.position in self.snake.positions:
                    self.nourriture.generer()
    
    def dessiner(self):
        self.ecran.fill(NOIR)
        
        if not self.game_over:
            self.snake.dessiner(self.ecran)
            self.nourriture.dessiner(self.ecran)
            
            # Afficher le score
            texte_score = self.font.render(f"Score: {self.score}", True, BLANC)
            self.ecran.blit(texte_score, (10, 10))
        else:
            # Écran de game over
            texte_game_over = self.font.render("GAME OVER", True, ROUGE)
            rect_go = texte_game_over.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 50))
            self.ecran.blit(texte_game_over, rect_go)
            
            texte_score_final = self.font.render(f"Score final: {self.score}", True, BLANC)
            rect_sf = texte_score_final.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
            self.ecran.blit(texte_score_final, rect_sf)
            
            texte_rejouer = self.font.render("Appuyez sur ESPACE pour rejouer", True, BLANC)
            rect_r = texte_rejouer.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 50))
            self.ecran.blit(texte_rejouer, rect_r)
        
        pygame.display.flip()
    
    def executer(self):
        en_cours = True
        while en_cours:
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()