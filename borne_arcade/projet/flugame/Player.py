import pygame
import math
from Bullet import Bullet
from Utils import *

class Player:
    def __init__(self):
        self.x = TILE_SIZE * (GRID_HEIGHT // 2)
        self.y = TILE_SIZE * (GRID_WIDTH  // 2)
        self.radius = 15
        self.speed = 4
        
        self.shoot_cooldown = 300      # tir normal
        self.spe_shoot_cooldown = 2000 # tir spécial plus long

        self.last_shot = 0
        self.last_special_shot = 0
        
        self.dir_x = 0
        self.dir_y = -1  # direction par défaut (haut)

    def try_move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy

        grid_x = int(new_x // TILE_SIZE)
        grid_y = int(new_y // TILE_SIZE)

        # Vérifie limites
        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if grid[grid_y][grid_x] == 0:
                self.x = new_x
                self.y = new_y

    def move(self, keys, grid):
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Si mouvement, on met à jour la direction
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            self.dir_x = dx / length
            self.dir_y = dy / length

            self.try_move(self.dir_x * self.speed,
                        self.dir_y * self.speed,
                        grid)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()

        if now - self.last_shot < self.shoot_cooldown:
            return

        if self.dir_x == 0 and self.dir_y == 0:
            return

        bullets.append(Bullet(self.x, self.y,
                            self.dir_x, self.dir_y))

        self.last_shot = now

    def radial_shot(self, bullets):
        now = pygame.time.get_ticks()

        if now - self.last_special_shot < self.spe_shoot_cooldown:
            return

        num_bullets = 8
        angle_step = 2 * math.pi / num_bullets

        for i in range(num_bullets):
            angle = i * angle_step
            dx = math.cos(angle)
            dy = math.sin(angle)

            bullets.append(Bullet(self.x, self.y, dx, dy))

        self.last_special_shot = now
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        
        cooldown_ratio = min(
            (pygame.time.get_ticks() - self.last_special_shot) / self.spe_shoot_cooldown, 1
        )

        bar_width = 40
        bar_height = 6

        pygame.draw.rect(screen, (50,50,50),
            (self.x - 20, self.y - 30, bar_width, bar_height))

        pygame.draw.rect(screen, (0,150,255),
            (self.x - 20, self.y - 30, bar_width * cooldown_ratio, bar_height))