"""Paramètres et constantes du jeu Snake."""

from __future__ import annotations

from typing import Final, Tuple

Color = Tuple[int, int, int]
Direction = Tuple[int, int]
Position = Tuple[int, int]

LARGEUR: Final[int] = 640
HAUTEUR: Final[int] = 480
TAILLE_CELLULE: Final[int] = 20
LIGNES: Final[int] = HAUTEUR // TAILLE_CELLULE
COLONNES: Final[int] = LARGEUR // TAILLE_CELLULE
FPS: Final[int] = 10

NOIR: Final[Color] = (0, 0, 0)
BLANC: Final[Color] = (255, 255, 255)
ROUGE: Final[Color] = (255, 0, 0)
VERT: Final[Color] = (0, 255, 0)
BLEU: Final[Color] = (0, 0, 255)
JAUNE: Final[Color] = (255, 255, 0)
VIOLET: Final[Color] = (255, 0, 255)
ORANGE: Final[Color] = (255, 165, 0)
MARRON: Final[Color] = (139, 69, 19)
GRIS: Final[Color] = (60, 60, 60)

HAUT: Final[Direction] = (0, -1)
BAS: Final[Direction] = (0, 1)
GAUCHE: Final[Direction] = (-1, 0)
DROITE: Final[Direction] = (1, 0)

__all__ = [
    "Color",
    "Direction",
    "Position",
    "LARGEUR",
    "HAUTEUR",
    "TAILLE_CELLULE",
    "LIGNES",
    "COLONNES",
    "FPS",
    "NOIR",
    "BLANC",
    "ROUGE",
    "VERT",
    "BLEU",
    "JAUNE",
    "VIOLET",
    "ORANGE",
    "MARRON",
    "GRIS",
    "HAUT",
    "BAS",
    "GAUCHE",
    "DROITE",
]
