import json
import pygame
import random
import sys
import colorsys
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 640
HAUTEUR = 480
TAILLE_CELLULE = 20
LIGNES = HAUTEUR // TAILLE_CELLULE
COLONNES = LARGEUR // TAILLE_CELLULE
FPS = 10

# Fichiers de données
DOSSIER_DONNEES = Path(__file__).resolve().parent / "data"
FICHIER_SCORES = DOSSIER_DONNEES / "scores.json"
FICHIER_SERPENTS = DOSSIER_DONNEES / "skins.json"
NB_SCORES_AFFICHES = 5


def charger_scores(fichier: Path = FICHIER_SCORES) -> list[int]:
    """Charge les scores sauvegardés depuis ``fichier``."""
    if not fichier.exists():
        return []

    try:
        with fichier.open("r", encoding="utf-8") as flux:
            donnees = json.load(flux)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(donnees, list):
        return []

    scores = []
    for valeur in donnees:
        try:
            scores.append(int(valeur))
        except (TypeError, ValueError):
            continue

    scores.sort(reverse=True)
    return scores


def sauvegarder_scores(scores: list[int], fichier: Path = FICHIER_SCORES) -> None:
    """Enregistre ``scores`` dans ``fichier`` (tri décroissant)."""
    fichier.parent.mkdir(parents=True, exist_ok=True)
    scores_triees = sorted((int(score) for score in scores), reverse=True)
    with fichier.open("w", encoding="utf-8") as flux:
        json.dump(scores_triees, flux, ensure_ascii=False, indent=2)


@dataclass(frozen=True)
class SnakeSkin:
    identifiant: str
    nom: str
    cout: int
    apparence: str
    effet: str
    couleur_mode: str = "rainbow"
    couleurs: tuple[tuple[int, int, int], ...] = tuple()
    options_snake: dict[str, Any] = field(default_factory=dict)


SNAKE_SKINS: tuple[SnakeSkin, ...] = (
    SnakeSkin(
        identifiant="orange",
        nom="Orange",
        cout=0,
        apparence="Serpent orange lumineux au style classique.",
        effet="Teinte unie pour une lisibilite immediate.",
        couleur_mode="palette",
        couleurs=((255, 165, 0),),
    ),
    SnakeSkin(
        identifiant="arc_en_ciel",
        nom="Arc-en-ciel",
        cout=0,
        apparence="Serpent prismatique aux couleurs changeantes.",
        effet="Animation lumineuse et dynamique.",
        couleur_mode="rainbow",
    ),
    SnakeSkin(
        identifiant="foret_de_jade",
        nom="Forêt de jade",
        cout=120,
        apparence="Dégradé de verts profonds inspiré de la canopée.",
        effet="Contour accentué et reflets atténués pour une meilleure lisibilité.",
        couleur_mode="palette",
        couleurs=(
            (34, 139, 34),
            (46, 180, 126),
            (144, 238, 144),
        ),
        options_snake={
            "AFFICHER_REFLET": False,
            "COULEUR_CONTOUR": (12, 60, 28),
            "LARGEUR_CONTOUR": 3,
        },
    ),
    SnakeSkin(
        identifiant="ocean_profond",
        nom="Océan profond",
        cout=180,
        apparence="Palette de bleus marins rappelant les profondeurs océaniques.",
        effet="Dégradé fluide entre nuances de bleu avec contour brillant.",
        couleur_mode="palette",
        couleurs=(
            (0, 105, 148),
            (30, 144, 255),
            (135, 206, 250),
        ),
        options_snake={
            "AFFICHER_REFLET": True,
            "COULEUR_CONTOUR": (0, 50, 80),
            "LARGEUR_CONTOUR": 2,
            "PALETTE_DEFILEMENT": 1.5,
        },
    ),
    SnakeSkin(
        identifiant="nocturne",
        nom="Nocturne",
        cout=250,
        apparence="Teintes nocturnes soulignées d'un halo électrique.",
        effet="Pulsation lumineuse rythmée et vitesse d'animation accrue.",
        couleur_mode="pulse",
        couleurs=((70, 70, 100),),
        options_snake={
            "AFFICHER_REFLET": False,
            "AFFICHER_OMBRE": False,
            "AFFICHER_CONTOUR": True,
            "COULEUR_CONTOUR": (180, 180, 255),
            "VITESSE_ANIMATION": 0.45,
            "PULSE_VITESSE": 2.2,
            "PULSE_AMPLITUDE": 0.55,
            "PULSE_DECALE": 0.35,
        },
    ),
    SnakeSkin(
        identifiant="magma",
        nom="Magma",
        cout=350,
        apparence="Serpent incandescent évoquant la lave en fusion.",
        effet="Pulsation rouge-orange intense avec effet de chaleur.",
        couleur_mode="pulse",
        couleurs=((180, 50, 30),),
        options_snake={
            "AFFICHER_REFLET": False,
            "AFFICHER_OMBRE": True,
            "AFFICHER_CONTOUR": True,
            "COULEUR_CONTOUR": (255, 140, 0),
            "COULEUR_OMBRE": (255, 69, 0, 80),
            "VITESSE_ANIMATION": 0.35,
            "PULSE_VITESSE": 3.0,
            "PULSE_AMPLITUDE": 0.7,
            "PULSE_DECALE": 0.2,
        },
    ),
    SnakeSkin(
        identifiant="desert_royal",
        nom="Désert royal",
        cout=400,
        apparence="Tons chauds du désert avec éclat doré.",
        effet="Palette or et sable avec reflets intenses.",
        couleur_mode="palette",
        couleurs=(
            (218, 165, 32),
            (255, 215, 0),
            (255, 235, 140),
        ),
        options_snake={
            "AFFICHER_REFLET": True,
            "COULEUR_CONTOUR": (139, 90, 0),
            "LARGEUR_CONTOUR": 3,
            "COULEUR_REFLET": (255, 255, 200, 80),
            "PALETTE_DEFILEMENT": 2.0,
        },
    ),
    SnakeSkin(
        identifiant="venimeux",
        nom="Venimeux",
        cout=500,
        apparence="Vert toxique lumineux avec effet d'avertissement.",
        effet="Pulsation acide rapide évoquant le danger.",
        couleur_mode="pulse",
        couleurs=((100, 200, 50),),
        options_snake={
            "AFFICHER_REFLET": False,
            "AFFICHER_OMBRE": False,
            "AFFICHER_CONTOUR": True,
            "COULEUR_CONTOUR": (200, 255, 0),
            "VITESSE_ANIMATION": 0.55,
            "PULSE_VITESSE": 4.0,
            "PULSE_AMPLITUDE": 0.6,
            "PULSE_DECALE": 0.15,
        },
    ),
    SnakeSkin(
        identifiant="cristal",
        nom="Cristal",
        cout=600,
        apparence="Serpent translucide aux couleurs pastel cristallines.",
        effet="Palette douce avec effets de transparence et brillance.",
        couleur_mode="palette",
        couleurs=(
            (200, 180, 255),
            (180, 220, 255),
            (220, 200, 255),
        ),
        options_snake={
            "AFFICHER_REFLET": True,
            "COULEUR_CONTOUR": (150, 130, 200),
            "LARGEUR_CONTOUR": 2,
            "COULEUR_REFLET": (255, 255, 255, 100),
            "PALETTE_DEFILEMENT": 1.0,
        },
    ),
    SnakeSkin(
        identifiant="galaxie",
        nom="Galaxie",
        cout=750,
        apparence="Serpent cosmique scintillant aux teintes galactiques.",
        effet="Arc-en-ciel ralenti avec effet étoilé mystique.",
        couleur_mode="rainbow",
        options_snake={
            "AFFICHER_REFLET": True,
            "COULEUR_CONTOUR": (50, 0, 100),
            "LARGEUR_CONTOUR": 3,
            "VITESSE_ANIMATION": 0.15,
            "COULEUR_REFLET": (255, 255, 255, 120),
        },
    ),
)

SNAKE_SKINS_PAR_ID: dict[str, SnakeSkin] = {skin.identifiant: skin for skin in SNAKE_SKINS}
ID_SKIN_DEFAUT = SNAKE_SKINS[0].identifiant


def charger_progression_serpents(
    fichier: Path = FICHIER_SERPENTS,
) -> dict[str, Any]:
    """Charge les serpents débloqués et le serpent actif."""

    progression_defaut = {
        "achetes": [ID_SKIN_DEFAUT],
        "actif": ID_SKIN_DEFAUT,
    }

    if not fichier.exists():
        return progression_defaut

    try:
        with fichier.open("r", encoding="utf-8") as flux:
            donnees = json.load(flux)
    except (OSError, json.JSONDecodeError):
        return progression_defaut

    achetes = donnees.get("achetes")
    if not isinstance(achetes, list):
        achetes = []

    achetes_valides = []
    for identifiant in achetes:
        if isinstance(identifiant, str) and identifiant in SNAKE_SKINS_PAR_ID:
            achetes_valides.append(identifiant)

    if ID_SKIN_DEFAUT not in achetes_valides:
        achetes_valides.append(ID_SKIN_DEFAUT)

    actif = donnees.get("actif", ID_SKIN_DEFAUT)
    if actif not in SNAKE_SKINS_PAR_ID or actif not in achetes_valides:
        actif = ID_SKIN_DEFAUT

    return {
        "achetes": achetes_valides,
        "actif": actif,
    }


def sauvegarder_progression_serpents(
    achetes: list[str],
    actif: str,
    fichier: Path = FICHIER_SERPENTS,
) -> None:
    """Sauvegarde la progression des serpents débloqués."""

    if actif not in SNAKE_SKINS_PAR_ID:
        actif = ID_SKIN_DEFAUT

    uniques = []
    for identifiant in achetes:
        if identifiant in SNAKE_SKINS_PAR_ID and identifiant not in uniques:
            uniques.append(identifiant)

    if ID_SKIN_DEFAUT not in uniques:
        uniques.append(ID_SKIN_DEFAUT)

    fichier.parent.mkdir(parents=True, exist_ok=True)
    with fichier.open("w", encoding="utf-8") as flux:
        json.dump({"achetes": uniques, "actif": actif}, flux, ensure_ascii=False, indent=2)

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
VIOLET = (255, 0, 255)
ORANGE = (255, 165, 0)
MARRON = (139, 69, 19)
GRIS = (60, 60, 60)
ROSE = (255, 105, 180)
VERT_FEUILLE = (46, 139, 87)

# Directions
HAUT = (0, -1)
BAS = (0, 1)
GAUCHE = (-1, 0)
DROITE = (1, 0)


class Snake:
    # Constantes d'animation (éviter les magic numbers)
    VITESSE_ANIMATION = 0.25  # cycles par seconde
    DELTA_COULEUR = 0.10      # espacement de teinte entre segments
    AFFICHER_CONTOUR = True   # contour optionnel pour la lisibilité

    # Palette et rendu (rafraîchissement visuel)
    COULEUR_CONTOUR = (40, 40, 40)  # gris anthracite : contraste doux sur le fond noir
    LARGEUR_CONTOUR = 2             # intensité du contour (px)
    COULEUR_OMBRE = (0, 0, 0, 110)  # ombre portée diffuse
    DECALAGE_OMBRE = (3, 3)         # décalage de l'ombre (x, y)
    AFFICHER_OMBRE = True
    COULEUR_REFLET = (255, 255, 255, 45)  # reflet léger pour donner du volume
    AFFICHER_REFLET = True

    # Géométrie des segments
    RAYON_ANGLE_CORPS = 6
    RAYON_ANGLE_TETE = 8
    ECLAT_TETE = 0.18              # renforce légèrement la luminosité de la tête
    ECLAT_MUSEAU = 0.32            # museau plus clair pour le volume
    DECALAGE_MUSEAU = 4
    RAYON_MUSEAU = 4

    # Animation des yeux (directionnelle)
    COULEUR_YEUX = (250, 250, 250)
    COULEUR_PUPILLE = (25, 25, 25)
    RAYON_YEUX = 4
    RAYON_PUPILLE = 2
    ECART_YEUX = 4                 # espacement latéral entre les yeux
    DISTANCE_DIRECTION_YEUX = 4    # décalage des yeux vers l'avant
    DECALAGE_PUPILLE = 2           # déplacement des pupilles vers la direction
    def __init__(self, skin: SnakeSkin | None = None):
        self.skin = skin or SNAKE_SKINS_PAR_ID[ID_SKIN_DEFAUT]
        self.positions = [(COLONNES // 2, LIGNES // 2)]
        self.direction = DROITE
        self.grandir = False
        self._palette_couleurs = tuple(self.skin.couleurs)
        self._options_skin = dict(self.skin.options_snake)

        for attribut, valeur in self._options_skin.items():
            setattr(self, attribut, valeur)
        
    def _couleur_arc_en_ciel(self, index_segment: int, current_time: float | None = None) -> tuple:
        """Retourne une couleur arc‑en‑ciel (RGB) pour un segment.
        L'effet est animé dans le temps et décalé par segment.
        """
        # Décalage temporel pour l'animation (secondes)
        if current_time is None:
            current_time = pygame.time.get_ticks() / 1000.0
        # Vitesse de rotation des couleurs (cycles par seconde)
        vitesse = self.VITESSE_ANIMATION
        # Espacement de teinte entre segments
        delta = self.DELTA_COULEUR  # 0.0–1.0
        hue = (index_segment * delta + current_time * vitesse) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))

    def _couleur_palette(self, index_segment: int, current_time: float | None = None) -> tuple[int, int, int]:
        if not self._palette_couleurs:
            return self._couleur_arc_en_ciel(index_segment, current_time)

        palette = self._palette_couleurs
        if current_time is None:
            current_time = pygame.time.get_ticks() / 1000.0

        defilement = float(self._options_skin.get("PALETTE_DEFILEMENT", 0.0))
        decalage = 0
        if defilement:
            decalage = int(current_time * defilement) % len(palette)

        return palette[(index_segment + decalage) % len(palette)]

    def _couleur_pulse(self, index_segment: int, current_time: float | None = None) -> tuple[int, int, int]:
        base = self._palette_couleurs[0] if self._palette_couleurs else (100, 100, 100)
        if current_time is None:
            current_time = pygame.time.get_ticks() / 1000.0

        vitesse = float(self._options_skin.get("PULSE_VITESSE", 1.5))
        amplitude = float(self._options_skin.get("PULSE_AMPLITUDE", 0.4))
        decalage = float(self._options_skin.get("PULSE_DECALE", 0.25))
        phase = current_time * vitesse + index_segment * decalage
        intensite = (math.sin(phase) + 1) / 2

        return tuple(
            max(0, min(255, int(c + (255 - c) * amplitude * intensite)))
            for c in base
        )

    def _couleur_segment(self, index_segment: int, current_time: float | None = None) -> tuple[int, int, int]:
        mode = getattr(self.skin, "couleur_mode", "rainbow")
        if mode == "palette":
            return self._couleur_palette(index_segment, current_time)
        if mode == "pulse":
            return self._couleur_pulse(index_segment, current_time)
        return self._couleur_arc_en_ciel(index_segment, current_time)

    def _accentuer_couleur(self, couleur: tuple[int, int, int], boost: float) -> tuple[int, int, int]:
        """Éclaircit légèrement une couleur RGB."""
        return tuple(
            min(255, int(c + (255 - c) * boost))
            for c in couleur
        )
        
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
        # Cache la valeur temporelle pour cette frame
        current_time = pygame.time.get_ticks() / 1000.0
        for i, position in enumerate(self.positions):
            x = position[0] * TAILLE_CELLULE
            y = position[1] * TAILLE_CELLULE
            couleur = self._couleur_segment(i, current_time)

            est_tete = (i == 0)
            rayon = self.RAYON_ANGLE_TETE if est_tete else self.RAYON_ANGLE_CORPS
            if est_tete:
                couleur = self._accentuer_couleur(couleur, self.ECLAT_TETE)

            # Ombre portée pour du relief
            if self.AFFICHER_OMBRE:
                ombre_surface = pygame.Surface((TAILLE_CELLULE, TAILLE_CELLULE), pygame.SRCALPHA)
                pygame.draw.rect(
                    ombre_surface,
                    self.COULEUR_OMBRE,
                    ombre_surface.get_rect(),
                    border_radius=rayon,
                )
                ecran.blit(ombre_surface, (x + self.DECALAGE_OMBRE[0], y + self.DECALAGE_OMBRE[1]))

            segment_surface = pygame.Surface((TAILLE_CELLULE, TAILLE_CELLULE), pygame.SRCALPHA)
            rect = segment_surface.get_rect()
            pygame.draw.rect(segment_surface, couleur, rect, border_radius=rayon)

            if self.AFFICHER_REFLET:
                reflet_rect = pygame.Rect(0, 0, int(TAILLE_CELLULE * 0.65), int(TAILLE_CELLULE * 0.5))
                reflet_rect.x += 3
                reflet_rect.y += 2
                pygame.draw.ellipse(segment_surface, self.COULEUR_REFLET, reflet_rect)

            if self.AFFICHER_CONTOUR:
                pygame.draw.rect(
                    segment_surface,
                    self.COULEUR_CONTOUR,
                    rect,
                    width=self.LARGEUR_CONTOUR,
                    border_radius=rayon,
                )

            ecran.blit(segment_surface, (x, y))

            if est_tete:
                self._dessiner_tete(ecran, x, y, couleur)

    def _dessiner_tete(self, ecran, x: int, y: int, couleur: tuple[int, int, int]):
        """Ajoute museau et yeux orientés sur la tête du serpent."""
        centre_x = x + TAILLE_CELLULE // 2
        centre_y = y + TAILLE_CELLULE // 2
        dir_x, dir_y = self.direction

        # Museau légèrement plus clair dans la direction de déplacement
        museau_couleur = self._accentuer_couleur(couleur, self.ECLAT_MUSEAU)
        museau_centre = (
            centre_x + dir_x * self.DECALAGE_MUSEAU,
            centre_y + dir_y * self.DECALAGE_MUSEAU,
        )
        pygame.draw.circle(
            ecran,
            museau_couleur,
            (int(museau_centre[0]), int(museau_centre[1])),
            self.RAYON_MUSEAU,
        )

        # Calcul des yeux en fonction de la direction
        if dir_x != 0:
            avance = dir_x * self.DISTANCE_DIRECTION_YEUX
            lateral = self.ECART_YEUX
            yeux = [
                (centre_x + avance, centre_y - lateral),
                (centre_x + avance, centre_y + lateral),
            ]
            pupille_offset = (dir_x * self.DECALAGE_PUPILLE, 0)
        else:
            avance = dir_y * self.DISTANCE_DIRECTION_YEUX
            lateral = self.ECART_YEUX
            yeux = [
                (centre_x - lateral, centre_y + avance),
                (centre_x + lateral, centre_y + avance),
            ]
            pupille_offset = (0, dir_y * self.DECALAGE_PUPILLE)

        for oeil in yeux:
            pygame.draw.circle(ecran, self.COULEUR_YEUX, (int(oeil[0]), int(oeil[1])), self.RAYON_YEUX)
            pupille_centre = (oeil[0] + pupille_offset[0], oeil[1] + pupille_offset[1])
            pygame.draw.circle(
                ecran,
                self.COULEUR_PUPILLE,
                (int(pupille_centre[0]), int(pupille_centre[1])),
                self.RAYON_PUPILLE,
            )


class Nourriture:
    # Paramètres visuels pour la pomme
    RAYON_POMME = TAILLE_CELLULE // 2 - 3
    LARGEUR_REFLET = int(TAILLE_CELLULE * 0.35)
    HAUTEUR_REFLET = int(TAILLE_CELLULE * 0.25)
    LARGEUR_TIGE = 3
    HAUTEUR_TIGE = 6
    LARGEUR_FEUILLE = 6
    HAUTEUR_FEUILLE = 4

    def __init__(self):
        self.position = None
        # Sprite de la pomme pré‑rendu pour éviter une recréation à chaque frame
        self.sprite_nourriture = self._creer_sprite_pomme()
        self.generer()

    def generer(self):
        self.position = (random.randint(0, COLONNES - 1),
                        random.randint(0, LIGNES - 1))

    def _creer_sprite_pomme(self):
        surf = pygame.Surface((TAILLE_CELLULE, TAILLE_CELLULE), pygame.SRCALPHA).convert_alpha()

        centre = (TAILLE_CELLULE // 2, TAILLE_CELLULE // 2 + 2)

        # Corps principal de la pomme
        pygame.draw.circle(surf, ROSE, centre, self.RAYON_POMME)

        # Légère variation pour simuler le volume
        reflet_rect = pygame.Rect(0, 0, self.LARGEUR_REFLET, self.HAUTEUR_REFLET)
        reflet_rect.center = (centre[0] - self.RAYON_POMME // 2, centre[1] - self.RAYON_POMME // 2)
        reflet_couleur = (min(255, ROSE[0] + 20), min(255, ROSE[1] + 20), min(255, ROSE[2] + 20), 160)
        pygame.draw.ellipse(surf, reflet_couleur, reflet_rect)

        # Tige
        tige_rect = pygame.Rect(0, 0, self.LARGEUR_TIGE, self.HAUTEUR_TIGE)
        tige_rect.center = (centre[0], centre[1] - self.RAYON_POMME - self.HAUTEUR_TIGE // 2 + 2)
        pygame.draw.rect(surf, MARRON, tige_rect)

        # Feuille verte à côté de la tige
        feuille_rect = pygame.Rect(0, 0, self.LARGEUR_FEUILLE, self.HAUTEUR_FEUILLE)
        feuille_rect.midleft = (tige_rect.right, tige_rect.top)
        pygame.draw.ellipse(surf, VERT_FEUILLE, feuille_rect)

        return surf

    def dessiner(self, ecran):
        # Afficher la pomme pré‑rendue
        x = self.position[0] * TAILLE_CELLULE
        y = self.position[1] * TAILLE_CELLULE
        ecran.blit(self.sprite_nourriture, (x, y))


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
        self.font = pygame.font.Font(None, 36)
        self.font_moyen = pygame.font.Font(None, 30)
        self.font_petit = pygame.font.Font(None, 24)
        self.scores = charger_scores()
        self.meilleur_score = self.scores[0] if self.scores else 0

        progression = charger_progression_serpents()
        self.skins_debloques = set(progression["achetes"])
        skin_active = progression.get("actif", ID_SKIN_DEFAUT)
        self.skin_selectionnee = SNAKE_SKINS_PAR_ID.get(skin_active, SNAKE_SKINS_PAR_ID[ID_SKIN_DEFAUT])
        if self.skin_selectionnee.identifiant not in self.skins_debloques:
            self.skin_selectionnee = SNAKE_SKINS_PAR_ID[ID_SKIN_DEFAUT]
            self.skins_debloques.add(self.skin_selectionnee.identifiant)

        self.index_menu_selection = self._trouver_index_skin(self.skin_selectionnee.identifiant)
        self.message_menu = ""
        self.message_menu_couleur = BLANC

        self.snake: Snake | None = None
        self.nourriture: Nourriture | None = None
        self.bonus: Bonus | None = None
        self.score = 0
        self.niveau = 1
        self.multiplicateur_score = 1
        self.vitesse_actuelle = FPS
        self.invincible = False
        self.temps_invincible = 0
        self.temps_multiplicateur = 0
        self.frame_count = 0
        self.score_enregistre = False
        self.etat = "menu"

    def _trouver_index_skin(self, identifiant: str) -> int:
        for index, skin in enumerate(SNAKE_SKINS):
            if skin.identifiant == identifiant:
                return index
        return 0

    def _mettre_a_jour_meilleur_score(self) -> None:
        self.meilleur_score = max(self.scores) if self.scores else 0

    def _sauvegarder_progression(self) -> None:
        ordre = sorted(
            self.skins_debloques,
            key=lambda ident: (SNAKE_SKINS_PAR_ID[ident].cout, ident),
        )
        sauvegarder_progression_serpents(list(ordre), self.skin_selectionnee.identifiant)

    def _peut_acheter_skin(self, skin: SnakeSkin) -> bool:
        if skin.identifiant in self.skins_debloques:
            return True
        return self.meilleur_score >= skin.cout

    def _valider_selection_skin(self) -> None:
        skin = SNAKE_SKINS[self.index_menu_selection]
        if skin.identifiant in self.skins_debloques:
            self.skin_selectionnee = skin
            self.message_menu = f"{skin.nom} sélectionné"
            self.message_menu_couleur = VERT
            self._sauvegarder_progression()
            return

        if self._peut_acheter_skin(skin):
            self.skins_debloques.add(skin.identifiant)
            self.skin_selectionnee = skin
            self.message_menu = f"{skin.nom} débloqué !"
            self.message_menu_couleur = ORANGE
            self._sauvegarder_progression()
        else:
            self.message_menu = "Score insuffisant pour débloquer ce serpent."
            self.message_menu_couleur = ROUGE

    def _initialiser_nouvelle_partie(self) -> None:
        self.snake = Snake(self.skin_selectionnee)
        self.nourriture = Nourriture()
        self.bonus = None
        self.score = 0
        self.niveau = 1
        self.multiplicateur_score = 1
        self.vitesse_actuelle = FPS
        self.invincible = False
        self.temps_invincible = 0
        self.temps_multiplicateur = 0
        self.frame_count = 0
        self.score_enregistre = False
        self.etat = "jeu"
        self.message_menu = ""

    def _retour_menu_depuis_game_over(self) -> None:
        self.etat = "menu"
        self.index_menu_selection = self._trouver_index_skin(self.skin_selectionnee.identifiant)
        self.message_menu = ""
        self.message_menu_couleur = BLANC
        self.vitesse_actuelle = FPS
        self.snake = None
        self.nourriture = None
        self.bonus = None

    def _dessiner_menu(self) -> None:
        self.ecran.fill((15, 15, 18))

        titre = self.font_moyen.render("Sélection des serpents", True, BLANC)
        self.ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 30)))

        instructions = self.font_petit.render(
            "↑↓ : naviguer  •  ENTRÉE : sélectionner  •  ESPACE : jouer",
            True,
            GRIS,
        )
        self.ecran.blit(instructions, instructions.get_rect(center=(LARGEUR // 2, 55)))

        meilleur = self.font_petit.render(f"Meilleur score : {self.meilleur_score}", True, BLANC)
        self.ecran.blit(meilleur, (40, 75))

        base_y = 100
        ligne = 38
        for index, skin in enumerate(SNAKE_SKINS):
            y = base_y + index * ligne
            rect = pygame.Rect(40, y - 8, LARGEUR - 80, 40)
            if index == self.index_menu_selection:
                pygame.draw.rect(self.ecran, (45, 45, 60), rect, border_radius=10)

            debloque = skin.identifiant in self.skins_debloques
            actif = skin.identifiant == self.skin_selectionnee.identifiant

            if not debloque:
                couleur_nom = GRIS
            elif actif:
                couleur_nom = VERT
            else:
                couleur_nom = BLANC

            nom_surface = self.font_petit.render(f"{skin.nom} - {skin.cout} pts", True, couleur_nom)
            self.ecran.blit(nom_surface, (rect.x + 12, rect.y + 4))

            if actif and debloque:
                statut = ("Actif", VERT)
            elif debloque:
                statut = ("Débloqué", BLANC)
            elif self._peut_acheter_skin(skin):
                statut = ("Achetable", JAUNE)
            else:
                statut = ("Verrouillé", ROUGE)

            statut_surface = self.font_petit.render(statut[0], True, statut[1])
            self.ecran.blit(statut_surface, (rect.x + 12, rect.y + 20))

        if self.message_menu:
            message_surface = self.font_petit.render(self.message_menu, True, self.message_menu_couleur)
            message_rect = message_surface.get_rect(center=(LARGEUR // 2, HAUTEUR - 15))
            self.ecran.blit(message_surface, message_rect)

    def _enregistrer_score_si_necessaire(self):
        if not self.score_enregistre:
            self.scores.append(self.score)
            self.scores.sort(reverse=True)
            sauvegarder_scores(self.scores)
            self.score_enregistre = True
            self._mettre_a_jour_meilleur_score()

    def _scores_a_afficher(self) -> list[tuple[str, int, bool]]:
        scores_affiches: list[tuple[str, int, bool]] = []
        score_courant_marque = False

        for indice, score in enumerate(self.scores[:NB_SCORES_AFFICHES], start=1):
            est_courant = False
            if not score_courant_marque and score == self.score:
                est_courant = True
                score_courant_marque = True
            scores_affiches.append((f"{indice}.", score, est_courant))

        if not score_courant_marque:
            scores_affiches.append(("Vous", self.score, True))

        if not scores_affiches:
            scores_affiches.append(("Vous", self.score, True))

        return scores_affiches
        
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            elif evenement.type == pygame.KEYDOWN:
                if self.etat == "menu":
                    if evenement.key in (pygame.K_UP, pygame.K_w):
                        self.index_menu_selection = (self.index_menu_selection - 1) % len(SNAKE_SKINS)
                        self.message_menu = ""
                        self.message_menu_couleur = BLANC
                    elif evenement.key in (pygame.K_DOWN, pygame.K_s):
                        self.index_menu_selection = (self.index_menu_selection + 1) % len(SNAKE_SKINS)
                        self.message_menu = ""
                        self.message_menu_couleur = BLANC
                    elif evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self._valider_selection_skin()
                    elif evenement.key == pygame.K_SPACE:
                        skin = SNAKE_SKINS[self.index_menu_selection]
                        if skin.identifiant not in self.skins_debloques:
                            self.message_menu = "Ce serpent est verrouillé."
                            self.message_menu_couleur = ROUGE
                        else:
                            if skin.identifiant != self.skin_selectionnee.identifiant:
                                self.skin_selectionnee = skin
                                self._sauvegarder_progression()
                            self._initialiser_nouvelle_partie()
                elif self.etat == "jeu":
                    if not self.snake:
                        continue
                    if evenement.key == pygame.K_UP:
                        self.snake.changer_direction(HAUT)
                    elif evenement.key == pygame.K_DOWN:
                        self.snake.changer_direction(BAS)
                    elif evenement.key == pygame.K_LEFT:
                        self.snake.changer_direction(GAUCHE)
                    elif evenement.key == pygame.K_RIGHT:
                        self.snake.changer_direction(DROITE)
                    elif evenement.key == pygame.K_ESCAPE:
                        self._retour_menu_depuis_game_over()
                elif self.etat == "game_over":
                    if evenement.key == pygame.K_SPACE:
                        self._retour_menu_depuis_game_over()
        return True
    
    def mettre_a_jour(self):
        if self.etat != "jeu" or not self.snake or not self.nourriture:
            return

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
                self.etat = "game_over"
                self._enregistrer_score_si_necessaire()
                return
            # En mode invincible, téléporter de l'autre côté
            tete = self.snake.positions[0]
            if tete in self.snake.positions[1:]:
                self.etat = "game_over"
                self._enregistrer_score_si_necessaire()
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
        if self.etat == "menu":
            self._dessiner_menu()
            pygame.display.flip()
            return

        self.ecran.fill(NOIR)

        if self.etat == "jeu" and self.snake and self.nourriture:
            # Effet visuel pour l'invincibilité
            if self.invincible and self.temps_invincible % 10 < 5:
                pygame.draw.rect(self.ecran, ORANGE, (0, 0, LARGEUR, HAUTEUR), 3)

            self.snake.dessiner(self.ecran)
            self.nourriture.dessiner(self.ecran)

            if self.bonus:
                self.bonus.dessiner(self.ecran)

            texte_score = self.font.render(f"Score: {self.score}", True, BLANC)
            self.ecran.blit(texte_score, (10, 10))

            texte_niveau = self.font_petit.render(f"Niveau: {self.niveau}", True, BLANC)
            self.ecran.blit(texte_niveau, (10, 50))

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

        elif self.etat == "game_over":
            texte_game_over = self.font.render("GAME OVER", True, ROUGE)
            rect_go = texte_game_over.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 60))
            self.ecran.blit(texte_game_over, rect_go)

            texte_score_final = self.font.render(f"Score final: {self.score}", True, BLANC)
            rect_sf = texte_score_final.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 10))
            self.ecran.blit(texte_score_final, rect_sf)

            skin_actif = self.font_petit.render(f"Serpent: {self.skin_selectionnee.nom}", True, BLANC)
            rect_skin = skin_actif.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 20))
            self.ecran.blit(skin_actif, rect_skin)

            texte_rejouer = self.font.render("ESPACE pour retourner au menu", True, BLANC)
            rect_r = texte_rejouer.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 70))
            self.ecran.blit(texte_rejouer, rect_r)

            titre_scores = self.font.render("Top scores", True, BLANC)
            rect_titre = titre_scores.get_rect()
            rect_titre.midtop = (LARGEUR // 2, rect_r.bottom + 30)
            self.ecran.blit(titre_scores, rect_titre)

            y_ligne = rect_titre.bottom + 10
            for etiquette, score, est_courant in self._scores_a_afficher():
                separateur = ":" if not etiquette.endswith(".") else ""
                texte = f"{etiquette}{separateur} {score}"
                couleur = VERT if est_courant else BLANC
                rendu = self.font_petit.render(texte, True, couleur)
                rect_ligne = rendu.get_rect()
                rect_ligne.midtop = (LARGEUR // 2, y_ligne)
                self.ecran.blit(rendu, rect_ligne)
                y_ligne += 24

        pygame.display.flip()
    
    def executer(self):
        en_cours = True
        while en_cours:
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            cadence = self.vitesse_actuelle if self.etat == "jeu" else FPS
            self.horloge.tick(cadence)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()
