"""
Jeu sidescroller – "Chat vs Chiens"
====================================
Le joueur contrôle un chat qui doit traverser une ville pleine de chiens.

• Flèches Gauche / Droite : se déplacer
• ESPACE : saut (et wall‑jump si collé à un mur)
• R : recommencer après un game over

Dépendances : Pygame ≥ 2.0
Installez‑les avec :
    pip install pygame

Exécution :
    python sidescroller_chat.py
"""
import pygame
import sys
import random
from typing import List

# -----------------------
# Constantes du jeu
# -----------------------
WIDTH, HEIGHT = 960, 540
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -16
WALL_JUMP_POWER_X = 10
WALL_JUMP_POWER_Y = -14
PLAYER_SPEED = 6
SCROLL_EDGE = WIDTH // 3  # déclenche le scrolling quand le joueur s'en approche

# Couleurs (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (80, 80, 80)      # plateformes

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Chat vs Chiens – Sidescroller")
font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 36)

# Chargement des images
CAT_SHEET_PATH = "Imagesidescroller/Chatanimation.png"
DOG_SHEET_PATH = "Imagesidescroller/Chienanimation.png"
BG_IMG_PATHS = [f"Imagesidescroller/Background ({i}).png" for i in range(1, 5)]

cat_sheet = pygame.image.load(CAT_SHEET_PATH).convert_alpha()
dog_sheet = pygame.image.load(DOG_SHEET_PATH).convert_alpha()
background_frames = [
    pygame.transform.scale(pygame.image.load(p).convert(), (WIDTH, HEIGHT))
    for p in BG_IMG_PATHS
]

# -----------------------
# Classes principales
# -----------------------
class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = 0
        self.vy = 0

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 50)
        self.on_ground = False
        self.touching_left_wall = False
        self.touching_right_wall = False
        # Animation
        sheet_w, sheet_h = cat_sheet.get_size()
        fw = sheet_w // 6
        fh = sheet_h // 4
        self.idle_frame = pygame.transform.scale(
            cat_sheet.subsurface(pygame.Rect(0, 0, fw, fh)), (40, 50)
        )
        self.walk_frames = [
            pygame.transform.scale(
                cat_sheet.subsurface(pygame.Rect(i * fw, fh, fw, fh)),
                (40, 50),
            )
            for i in range(6)
        ]
        self.jump_frame = pygame.transform.scale(
            cat_sheet.subsurface(pygame.Rect(0, 2 * fh, fw, fh)), (40, 50)
        )
        self.wall_frame = pygame.transform.scale(
            cat_sheet.subsurface(pygame.Rect(0, 3 * fh, fw, fh)), (40, 50)
        )
        self.anim_index = 0
        self.direction = 1
        self.image = self.idle_frame

    def update(self, platforms: List[pygame.Rect]):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED

        # Saut
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.vy = JUMP_POWER
            elif self.touching_left_wall:
                self.vx = WALL_JUMP_POWER_X
                self.vy = WALL_JUMP_POWER_Y
            elif self.touching_right_wall:
                self.vx = -WALL_JUMP_POWER_X
                self.vy = WALL_JUMP_POWER_Y

        if self.vx != 0:
            self.direction = 1 if self.vx > 0 else -1

        # Appliquer la gravité
        self.vy += GRAVITY
        if self.vy > 20:
            self.vy = 20

        # Déplacement horizontal puis résolution de collision latérale
        self.rect.x += self.vx
        self.touching_left_wall = self.touching_right_wall = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                    self.touching_right_wall = True
                elif self.vx < 0:
                    self.rect.left = plat.right
                    self.touching_left_wall = True

        # Déplacement vertical puis résolution de collision verticale
        self.rect.y += self.vy
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                    self.vy = 0

        self.animate()

    def animate(self):
        if not self.on_ground:
            if self.touching_left_wall or self.touching_right_wall:
                frame = self.wall_frame
            else:
                frame = self.jump_frame
        elif self.vx != 0:
            self.anim_index = (self.anim_index + 1) % (len(self.walk_frames) * 6)
            frame = self.walk_frames[self.anim_index // 6]
        else:
            frame = self.idle_frame

        self.image = pygame.transform.flip(frame, self.direction < 0, False)

class Dog(Entity):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(x, y, 50, 40)
        sheet_w, sheet_h = dog_sheet.get_size()
        fw = sheet_w // 6
        fh = sheet_h // 4
        self.frames = [
            pygame.transform.scale(
                dog_sheet.subsurface(pygame.Rect(i * fw, 0, fw, fh)), (50, 40)
            )
            for i in range(6)
        ]
        self.anim_index = 0
        self.image = self.frames[0]
        self.direction = 1
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vx = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.vx
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vx *= -1
        self.direction = 1 if self.vx > 0 else -1
        self.anim_index = (self.anim_index + 1) % (len(self.frames) * 6)
        frame = self.frames[self.anim_index // 6]
        self.image = pygame.transform.flip(frame, self.direction < 0, False)

# -----------------------
# Niveau
# -----------------------
class Level:
    def __init__(self):
        self.platforms = []  # liste de Rect
        self.enemies = pygame.sprite.Group()
        self.length = 4000  # longueur totale du niveau en pixels
        self.bg_frames = background_frames
        self.bg_index = 0
        self.build_level()

    def build_level(self):
        # Sol continu
        self.platforms.append(pygame.Rect(0, HEIGHT - 40, self.length, 40))

        # Quelques plateformes et murs
        structure = [
            (400, 380, 200, 20),
            (800, 300, 180, 20),
            (1200, 220, 220, 20),
            (1600, 150, 160, 20),
            # murs verticaux pour wall‑jump
            (950, HEIGHT - 200, 20, 160),
            (1400, HEIGHT - 260, 20, 220),
        ]
        for x, y, w, h in structure:
            self.platforms.append(pygame.Rect(x, y, w, h))

        # Ajouter des chiens
        dogs_specs = [
            (600, HEIGHT - 80, 500, 700),
            (1100, HEIGHT - 80, 1000, 1300),
            (1900, HEIGHT - 80, 1800, 2000),
            (2600, HEIGHT - 80, 2500, 2800),
        ]
        for x, y, l, r in dogs_specs:
            self.enemies.add(Dog(x, y, l, r))

    def draw(self, surface, camera_x):
        # Dessiner l'arrière-plan
        frame = self.bg_frames[int(self.bg_index) % len(self.bg_frames)]
        surface.blit(frame, (0, 0))
        # Dessiner plateformes
        for plat in self.platforms:
            pygame.draw.rect(surface, GREY, pygame.Rect(plat.x - camera_x, plat.y, plat.width, plat.height))
        # Dessiner ennemis
        for enemy in self.enemies:
            surface.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))

    def update(self):
        self.bg_index += 0.1
        for enemy in self.enemies:
            enemy.update()

# -----------------------
# Boucle principale
# -----------------------

def reset_game():
    player = Player(50, HEIGHT - 100)
    level = Level()
    camera_x = 0
    return player, level, camera_x

player, level, camera_x = reset_game()
game_over = False
score = 0

while True:
    dt = clock.tick(FPS) / 1000  # seconds per frame (peut servir pour des mouvements plus précis)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            player, level, camera_x = reset_game()
            game_over = False
            score = 0

    if not game_over:
        # Mise à jour logique
        player.update(level.platforms)
        level.update()
        score = max(score, player.rect.x)

        # Collision joueur‑ennemi
        for enemy in level.enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True
                break

        # Victoire si on atteint la fin du niveau
        if player.rect.x >= level.length - 200:
            game_over = True

        # Gestion du scrolling caméra
        if player.rect.x - camera_x > SCROLL_EDGE:
            camera_x = player.rect.x - SCROLL_EDGE
        if player.rect.x - camera_x < SCROLL_EDGE // 2 and camera_x > 0:
            camera_x = max(0, player.rect.x - SCROLL_EDGE // 2)

    # -------------------------------------
    # Rendu
    # -------------------------------------
    level.draw(screen, camera_x)
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
    score_surf = score_font.render(f"Score : {score}", True, BLACK)
    screen.blit(score_surf, (10, 10))

    if game_over:
        if player.rect.x >= level.length - 200:
            txt = font.render("Gagné !", True, BLACK)
        else:
            txt = font.render("Game Over", True, BLACK)
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        info = font.render("Appuie sur R pour recommencer", True, BLACK)
        screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        final_score = font.render(f"Score : {score}", True, BLACK)
        screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))

    pygame.display.flip()
