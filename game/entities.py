"""Entités principales utilisées par le jeu Snake."""

from __future__ import annotations

import colorsys
import random
from typing import Optional, Sequence

import pygame

from . import settings

Surface = pygame.Surface
Position = settings.Position
Direction = settings.Direction


class Snake:
    """Représente le serpent contrôlé par le joueur."""

    VITESSE_ANIMATION: float = 0.25
    DELTA_COULEUR: float = 0.10
    AFFICHER_CONTOUR: bool = True

    def __init__(self) -> None:
        self.positions: list[Position] = [(settings.COLONNES // 2, settings.LIGNES // 2)]
        self.direction: Direction = settings.DROITE
        self.grandir: bool = False

    def _couleur_arc_en_ciel(self, index_segment: int, current_time: Optional[float] = None) -> settings.Color:
        """Calcule une couleur arc-en-ciel animée pour un segment du serpent."""
        if current_time is None:
            current_time = pygame.time.get_ticks() / 1000.0
        vitesse = self.VITESSE_ANIMATION
        delta = self.DELTA_COULEUR
        hue = (index_segment * delta + current_time * vitesse) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))

    def bouger(self) -> bool:
        """Déplace le serpent d'une case.

        Retourne ``False`` en cas de collision avec un mur ou avec lui-même.
        """
        tete = self.positions[0]
        nouvelle_tete = (tete[0] + self.direction[0], tete[1] + self.direction[1])

        if (nouvelle_tete[0] < 0 or nouvelle_tete[0] >= settings.COLONNES or
                nouvelle_tete[1] < 0 or nouvelle_tete[1] >= settings.LIGNES):
            return False

        if nouvelle_tete in self.positions:
            return False

        self.positions.insert(0, nouvelle_tete)

        if not self.grandir:
            self.positions.pop()
        else:
            self.grandir = False

        return True

    def changer_direction(self, nouvelle_direction: Direction) -> None:
        """Change la direction du serpent si le demi-tour est évité."""
        if (self.direction[0] * -1, self.direction[1] * -1) != nouvelle_direction:
            self.direction = nouvelle_direction

    def manger(self) -> None:
        """Indique que le serpent doit s'agrandir au prochain déplacement."""
        self.grandir = True

    def dessiner(self, ecran: Surface) -> None:
        """Dessine le serpent sur la surface fournie."""
        current_time = pygame.time.get_ticks() / 1000.0
        for index, position in enumerate(self.positions):
            x = position[0] * settings.TAILLE_CELLULE
            y = position[1] * settings.TAILLE_CELLULE
            couleur = self._couleur_arc_en_ciel(index, current_time)
            pygame.draw.rect(ecran, couleur, (x, y, settings.TAILLE_CELLULE, settings.TAILLE_CELLULE))
            if self.AFFICHER_CONTOUR:
                pygame.draw.rect(
                    ecran,
                    settings.GRIS,
                    (x, y, settings.TAILLE_CELLULE, settings.TAILLE_CELLULE),
                    1,
                )


class Nourriture:
    """Gère l'apparition et l'affichage de la nourriture."""

    BANANE_ANGLE_DEBUT: float = 0.7
    BANANE_ANGLE_FIN: float = 2.4
    BANANE_EPAISSEUR: int = 5
    BANANE_TIP_RAYON: int = 2

    def __init__(self) -> None:
        self.position: Optional[Position] = None
        self.sprite_banane: Surface = self._creer_sprite_banane()
        self.generer()

    def generer(self) -> None:
        """Positionne la nourriture sur une case aléatoire."""
        self.position = (
            random.randint(0, settings.COLONNES - 1),
            random.randint(0, settings.LIGNES - 1),
        )

    def _creer_sprite_banane(self) -> Surface:
        """Crée et retourne la surface représentant la banane."""
        surf = pygame.Surface((settings.TAILLE_CELLULE, settings.TAILLE_CELLULE), pygame.SRCALPHA).convert_alpha()
        rect_arc = pygame.Rect(2, 2, settings.TAILLE_CELLULE - 4, settings.TAILLE_CELLULE - 4)
        pygame.draw.arc(
            surf,
            settings.JAUNE,
            rect_arc,
            self.BANANE_ANGLE_DEBUT,
            self.BANANE_ANGLE_FIN,
            self.BANANE_EPAISSEUR,
        )
        tip1 = (rect_arc.left + 3, rect_arc.bottom - 6)
        tip2 = (rect_arc.right - 3, rect_arc.top + 6)
        pygame.draw.circle(surf, settings.MARRON, tip1, self.BANANE_TIP_RAYON)
        pygame.draw.circle(surf, settings.MARRON, tip2, self.BANANE_TIP_RAYON)
        return surf

    def dessiner(self, ecran: Surface) -> None:
        """Affiche la banane sur la surface passée en paramètre."""
        if self.position is None:
            return
        x = self.position[0] * settings.TAILLE_CELLULE
        y = self.position[1] * settings.TAILLE_CELLULE
        ecran.blit(self.sprite_banane, (x, y))


class Bonus:
    """Représente un bonus temporaire pouvant apparaître sur le plateau."""

    def __init__(self, type_bonus: str) -> None:
        self.type: str = type_bonus
        self.position: Optional[Position] = None
        self.duree_vie: int = 150
        self.couleur: settings.Color = {
            "vitesse": settings.JAUNE,
            "points": settings.VIOLET,
            "invincible": settings.ORANGE,
        }[type_bonus]

    def generer(self, positions_interdites: Sequence[Position]) -> None:
        """Positionne le bonus en évitant les cases interdites."""
        valide = False
        while not valide:
            self.position = (
                random.randint(0, settings.COLONNES - 1),
                random.randint(0, settings.LIGNES - 1),
            )
            if self.position not in positions_interdites:
                valide = True

    def mise_a_jour(self) -> bool:
        """Met à jour la durée de vie du bonus et indique s'il persiste."""
        self.duree_vie -= 1
        return self.duree_vie > 0

    def dessiner(self, ecran: Surface) -> None:
        """Dessine le bonus s'il est encore actif."""
        if self.position is None:
            return
        x = self.position[0] * settings.TAILLE_CELLULE
        y = self.position[1] * settings.TAILLE_CELLULE
        if self.duree_vie > 30 or self.duree_vie % 6 < 3:
            pygame.draw.circle(
                ecran,
                self.couleur,
                (x + settings.TAILLE_CELLULE // 2, y + settings.TAILLE_CELLULE // 2),
                settings.TAILLE_CELLULE // 2,
            )


__all__ = ["Snake", "Nourriture", "Bonus"]
