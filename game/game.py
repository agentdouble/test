"""Logique principale et boucle de jeu pour Snake."""

from __future__ import annotations

import random
import sys
from typing import Optional

import pygame

from . import settings
from .entities import Bonus, Nourriture, Snake


class Jeu:
    """Gère la boucle principale et l'état du jeu Snake."""

    def __init__(self) -> None:
        self.ecran: pygame.Surface = pygame.display.set_mode((settings.LARGEUR, settings.HAUTEUR))
        pygame.display.set_caption("Snake")
        self.horloge = pygame.time.Clock()
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.bonus: Optional[Bonus] = None
        self.score: int = 0
        self.niveau: int = 1
        self.multiplicateur_score: int = 1
        self.vitesse_actuelle: int = settings.FPS
        self.invincible: bool = False
        self.temps_invincible: int = 0
        self.temps_multiplicateur: int = 0
        self.font = pygame.font.Font(None, 36)
        self.font_petit = pygame.font.Font(None, 24)
        self.game_over: bool = False
        self.frame_count: int = 0

    def gerer_evenements(self) -> bool:
        """Traite la file d'événements Pygame."""
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            if evenement.type == pygame.KEYDOWN:
                if self.game_over:
                    if evenement.key == pygame.K_SPACE:
                        self.__init__()
                elif evenement.key == pygame.K_UP:
                    self.snake.changer_direction(settings.HAUT)
                elif evenement.key == pygame.K_DOWN:
                    self.snake.changer_direction(settings.BAS)
                elif evenement.key == pygame.K_LEFT:
                    self.snake.changer_direction(settings.GAUCHE)
                elif evenement.key == pygame.K_RIGHT:
                    self.snake.changer_direction(settings.DROITE)
        return True

    def mettre_a_jour(self) -> None:
        """Met à jour l'état du jeu pour la frame courante."""
        if self.game_over:
            return

        self.frame_count += 1

        if self.temps_invincible > 0:
            self.temps_invincible -= 1
            if self.temps_invincible == 0:
                self.invincible = False

        if self.temps_multiplicateur > 0:
            self.temps_multiplicateur -= 1
            if self.temps_multiplicateur == 0:
                self.multiplicateur_score = 1

        if not self.snake.bouger():
            if not self.invincible:
                self.game_over = True
                return
            tete = self.snake.positions[0]
            if tete in self.snake.positions[1:]:
                self.game_over = True
                return
            nouvelle_tete = list(tete)
            if tete[0] < 0:
                nouvelle_tete[0] = settings.COLONNES - 1
            elif tete[0] >= settings.COLONNES:
                nouvelle_tete[0] = 0
            if tete[1] < 0:
                nouvelle_tete[1] = settings.LIGNES - 1
            elif tete[1] >= settings.LIGNES:
                nouvelle_tete[1] = 0
            self.snake.positions[0] = tuple(nouvelle_tete)

        if self.snake.positions[0] == self.nourriture.position:
            self.snake.manger()
            self.score += 10 * self.multiplicateur_score

            if self.score % 50 == 0:
                self.niveau += 1
                self.vitesse_actuelle = min(settings.FPS + self.niveau * 2, 30)

            positions_interdites = self.snake.positions[:]
            if self.bonus and self.bonus.position is not None:
                positions_interdites.append(self.bonus.position)
            while self.nourriture.position in positions_interdites:
                self.nourriture.generer()

            if random.random() < 0.2 and self.bonus is None:
                type_bonus = random.choice(["vitesse", "points", "invincible"])
                self.bonus = Bonus(type_bonus)
                positions_pour_bonus = self.snake.positions[:]
                if self.nourriture.position is not None:
                    positions_pour_bonus.append(self.nourriture.position)
                self.bonus.generer(positions_pour_bonus)

        if self.bonus:
            if not self.bonus.mise_a_jour():
                self.bonus = None
            elif self.snake.positions[0] == self.bonus.position:
                if self.bonus.type == "vitesse":
                    self.vitesse_actuelle = max(5, self.vitesse_actuelle - 3)
                elif self.bonus.type == "points":
                    self.multiplicateur_score = 3
                    self.temps_multiplicateur = 100
                elif self.bonus.type == "invincible":
                    self.invincible = True
                    self.temps_invincible = 150

                self.score += 5 * self.multiplicateur_score
                self.bonus = None

    def dessiner(self) -> None:
        """Réalise le rendu complet de la frame courante."""
        self.ecran.fill(settings.NOIR)

        if not self.game_over:
            if self.invincible and self.temps_invincible % 10 < 5:
                pygame.draw.rect(self.ecran, settings.ORANGE, (0, 0, settings.LARGEUR, settings.HAUTEUR), 3)

            self.snake.dessiner(self.ecran)
            self.nourriture.dessiner(self.ecran)

            if self.bonus:
                self.bonus.dessiner(self.ecran)

            texte_score = self.font.render(f"Score: {self.score}", True, settings.BLANC)
            self.ecran.blit(texte_score, (10, 10))

            texte_niveau = self.font_petit.render(f"Niveau: {self.niveau}", True, settings.BLANC)
            self.ecran.blit(texte_niveau, (10, 50))

            y_effet = 80
            if self.multiplicateur_score > 1:
                texte_multi = self.font_petit.render(f"Points x{self.multiplicateur_score}", True, settings.VIOLET)
                self.ecran.blit(texte_multi, (10, y_effet))
                y_effet += 25

            if self.invincible:
                texte_invincible = self.font_petit.render("INVINCIBLE!", True, settings.ORANGE)
                self.ecran.blit(texte_invincible, (10, y_effet))
                y_effet += 25

            if self.vitesse_actuelle < settings.FPS:
                texte_vitesse = self.font_petit.render("Vitesse boost!", True, settings.JAUNE)
                self.ecran.blit(texte_vitesse, (10, y_effet))
        else:
            texte_game_over = self.font.render("GAME OVER", True, settings.ROUGE)
            rect_go = texte_game_over.get_rect(center=(settings.LARGEUR // 2, settings.HAUTEUR // 2 - 50))
            self.ecran.blit(texte_game_over, rect_go)

            texte_score_final = self.font.render(f"Score final: {self.score}", True, settings.BLANC)
            rect_sf = texte_score_final.get_rect(center=(settings.LARGEUR // 2, settings.HAUTEUR // 2))
            self.ecran.blit(texte_score_final, rect_sf)

            texte_rejouer = self.font.render("Appuyez sur ESPACE pour rejouer", True, settings.BLANC)
            rect_r = texte_rejouer.get_rect(center=(settings.LARGEUR // 2, settings.HAUTEUR // 2 + 50))
            self.ecran.blit(texte_rejouer, rect_r)

        pygame.display.flip()

    def executer(self) -> None:
        """Boucle principale du jeu."""
        en_cours = True
        while en_cours:
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(self.vitesse_actuelle)

        pygame.quit()
        sys.exit()


def main() -> None:
    """Point d'entrée pratique pour lancer le jeu Snake."""
    pygame.init()
    jeu = Jeu()
    jeu.executer()


__all__ = ["Jeu", "main"]
