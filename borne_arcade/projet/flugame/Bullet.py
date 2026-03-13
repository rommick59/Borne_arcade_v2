import pygame
from Utils import *

import pygame

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.speed = 8
        
        length = (dx**2 + dy**2) ** 0.5
        if length == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.dx = dx / length
            self.dy = dy / length

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000 

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def is_dead(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,0),
                           (int(self.x), int(self.y)), 5)