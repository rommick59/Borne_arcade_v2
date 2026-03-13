import pygame

TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#########
# création de la map 

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

for x in range(GRID_WIDTH):
    grid[0][x] = 1
    grid[GRID_HEIGHT - 1][x] = 1

for y in range(GRID_HEIGHT):
    grid[y][0] = 1
    grid[y][GRID_WIDTH - 1] = 1

center_x = GRID_WIDTH // 2
center_y = GRID_HEIGHT // 2
gap_size = 4
half_gap = gap_size // 2

for i in range(center_x - half_gap, center_x + half_gap):
    grid[0][i] = 0

for i in range(center_x - half_gap, center_x + half_gap):
    grid[GRID_HEIGHT - 1][i] = 0

for i in range(center_y - half_gap, center_y + half_gap):
    grid[i][0] = 0

for i in range(center_y - half_gap, center_y + half_gap):
    grid[i][GRID_WIDTH - 1] = 0

pillar_size = 2

positions = [
    (3, 3),
    (3, GRID_WIDTH - 5),
    (GRID_HEIGHT - 5, 3),
    (GRID_HEIGHT - 5, GRID_WIDTH - 5),
]

for py, px in positions:
    for y in range(py, py + pillar_size):
        for x in range(px, px + pillar_size):
            grid[y][x] = 1