import pygame
import random
import sys
import time
import colorsys

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
JAUNE = (255, 255, 0)
VIOLET = (255, 0, 255)
ORANGE = (255, 165, 0)

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
        
    def _couleur_arc_en_ciel(self, index_segment: int) -> tuple:
        """Retourne une couleur arc‑en‑ciel (RGB) pour un segment.
        L'effet est animé dans le temps et décalé par segment.
        """
        # Décalage temporel pour l'animation (secondes)
        t = pygame.time.get_ticks() / 1000.0
        # Vitesse de rotation des couleurs (cycles par seconde)
        vitesse = 0.25
        # Espacement de teinte entre segments
        delta = 0.10  # 0.0–1.0
        hue = (index_segment * delta + t * vitesse) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))
        
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
            couleur = self._couleur_arc_en_ciel(i)
            # Dessin principal
            pygame.draw.rect(ecran, couleur, (x, y, TAILLE_CELLULE, TAILLE_CELLULE))
            # Optionnel: léger contour pour mieux voir les couleurs sur fond sombre
            pygame.draw.rect(ecran, NOIR, (x, y, TAILLE_CELLULE, TAILLE_CELLULE), 1)


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


class Bonus:
    def __init__(self, type_bonus):
        self.type = type_bonus  # 'vitesse', 'points', 'invincible'
        self.position = None
        self.duree_vie = 150  # Disparaît après 150 frames
        self.couleur = {
            'vitesse': JAUNE,
            'points': VIOLET,
            'invincible': ORANGE
        }[type_bonus]
        
    def generer(self, positions_interdites):
        valide = False
        while not valide:
            self.position = (random.randint(0, COLONNES - 1), 
                            random.randint(0, LIGNES - 1))
            if self.position not in positions_interdites:
                valide = True
    
    def mise_a_jour(self):
        self.duree_vie -= 1
        return self.duree_vie > 0
    
    def dessiner(self, ecran):
        if self.position:
            x = self.position[0] * TAILLE_CELLULE
            y = self.position[1] * TAILLE_CELLULE
            # Effet de clignotement quand il va disparaître
            if self.duree_vie > 30 or self.duree_vie % 6 < 3:
                pygame.draw.circle(ecran, self.couleur, 
                                 (x + TAILLE_CELLULE // 2, y + TAILLE_CELLULE // 2), 
                                 TAILLE_CELLULE // 2)


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Snake")
        self.horloge = pygame.time.Clock()
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.bonus = None
        self.score = 0
        self.niveau = 1
        self.multiplicateur_score = 1
        self.vitesse_actuelle = FPS
        self.invincible = False
        self.temps_invincible = 0
        self.temps_multiplicateur = 0
        self.font = pygame.font.Font(None, 36)
        self.font_petit = pygame.font.Font(None, 24)
        self.game_over = False
        self.frame_count = 0
        
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
            self.frame_count += 1
            
            # Gérer les effets temporaires
            if self.temps_invincible > 0:
                self.temps_invincible -= 1
                if self.temps_invincible == 0:
                    self.invincible = False
                    
            if self.temps_multiplicateur > 0:
                self.temps_multiplicateur -= 1
                if self.temps_multiplicateur == 0:
                    self.multiplicateur_score = 1
            
            # Mouvement du serpent
            if not self.snake.bouger():
                if not self.invincible:
                    self.game_over = True
                    return
                else:
                    # En mode invincible, téléporter de l'autre côté
                    tete = self.snake.positions[0]
                    if tete in self.snake.positions[1:]:
                        self.game_over = True
                        return
                    nouvelle_tete = list(tete)
                    if tete[0] < 0:
                        nouvelle_tete[0] = COLONNES - 1
                    elif tete[0] >= COLONNES:
                        nouvelle_tete[0] = 0
                    if tete[1] < 0:
                        nouvelle_tete[1] = LIGNES - 1
                    elif tete[1] >= LIGNES:
                        nouvelle_tete[1] = 0
                    self.snake.positions[0] = tuple(nouvelle_tete)
            
            # Vérifier si le serpent mange la nourriture
            if self.snake.positions[0] == self.nourriture.position:
                self.snake.manger()
                self.score += 10 * self.multiplicateur_score
                
                # Augmenter le niveau tous les 50 points
                if self.score % 50 == 0:
                    self.niveau += 1
                    self.vitesse_actuelle = min(FPS + self.niveau * 2, 30)
                
                # Générer nouvelle nourriture
                positions_interdites = self.snake.positions[:]
                if self.bonus:
                    positions_interdites.append(self.bonus.position)
                while self.nourriture.position in positions_interdites:
                    self.nourriture.generer()
                
                # Chance de générer un bonus (20%)
                if random.random() < 0.2 and not self.bonus:
                    type_bonus = random.choice(['vitesse', 'points', 'invincible'])
                    self.bonus = Bonus(type_bonus)
                    self.bonus.generer(self.snake.positions + [self.nourriture.position])
            
            # Gérer les bonus
            if self.bonus:
                if not self.bonus.mise_a_jour():
                    self.bonus = None
                elif self.snake.positions[0] == self.bonus.position:
                    # Appliquer l'effet du bonus
                    if self.bonus.type == 'vitesse':
                        self.vitesse_actuelle = max(5, self.vitesse_actuelle - 3)
                    elif self.bonus.type == 'points':
                        self.multiplicateur_score = 3
                        self.temps_multiplicateur = 100
                    elif self.bonus.type == 'invincible':
                        self.invincible = True
                        self.temps_invincible = 150
                    
                    self.score += 5 * self.multiplicateur_score
                    self.bonus = None
    
    def dessiner(self):
        self.ecran.fill(NOIR)
        
        if not self.game_over:
            # Effet visuel pour l'invincibilité
            if self.invincible and self.temps_invincible % 10 < 5:
                # Bordure clignotante
                pygame.draw.rect(self.ecran, ORANGE, (0, 0, LARGEUR, HAUTEUR), 3)
            
            self.snake.dessiner(self.ecran)
            self.nourriture.dessiner(self.ecran)
            
            if self.bonus:
                self.bonus.dessiner(self.ecran)
            
            # Afficher les informations
            texte_score = self.font.render(f"Score: {self.score}", True, BLANC)
            self.ecran.blit(texte_score, (10, 10))
            
            texte_niveau = self.font_petit.render(f"Niveau: {self.niveau}", True, BLANC)
            self.ecran.blit(texte_niveau, (10, 50))
            
            # Afficher les effets actifs
            y_effet = 80
            if self.multiplicateur_score > 1:
                texte_multi = self.font_petit.render(f"Points x{self.multiplicateur_score}", True, VIOLET)
                self.ecran.blit(texte_multi, (10, y_effet))
                y_effet += 25
            
            if self.invincible:
                texte_invincible = self.font_petit.render("INVINCIBLE!", True, ORANGE)
                self.ecran.blit(texte_invincible, (10, y_effet))
                y_effet += 25
            
            if self.vitesse_actuelle < FPS:
                texte_vitesse = self.font_petit.render("Vitesse boost!", True, JAUNE)
                self.ecran.blit(texte_vitesse, (10, y_effet))
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
            self.horloge.tick(self.vitesse_actuelle)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()
