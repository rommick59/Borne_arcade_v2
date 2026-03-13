import pygame
from Utils import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, grid

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = 2

    def update(self, player, enemies):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            dx /= distance
            dy /= distance

        current_speed = self.speed

        self.try_move(dx * current_speed, dy * current_speed)

        self.separate(enemies)

    def try_move(self, dx, dy):
        new_x = self.x + dx
        grid_x = int(new_x // TILE_SIZE)
        grid_y = int(self.y // TILE_SIZE)

        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            if grid[grid_y][grid_x] == 0:
                self.x = new_x

        new_y = self.y + dy
        grid_x = int(self.x // TILE_SIZE)
        grid_y = int(new_y // TILE_SIZE)

        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            if grid[grid_y][grid_x] == 0:
                self.y = new_y

    def separate(self, enemies):
        push_x = 0
        push_y = 0

        for other in enemies:
            if other is self:
                continue

            dx = self.x - other.x
            dy = self.y - other.y
            distance = (dx**2 + dy**2) ** 0.5

            min_dist = self.radius + other.radius

            if distance < min_dist and distance != 0:
                overlap = min_dist - distance
                dx /= distance
                dy /= distance

                push_x += dx * overlap * 0.5
                push_y += dy * overlap * 0.5

        if push_x != 0 or push_y != 0:
            self.try_move(push_x, push_y)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0),
                           (int(self.x), int(self.y)),
                           self.radius)