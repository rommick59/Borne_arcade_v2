import pygame
import random
from Player import Player
from Enemy import Enemy
from Bullet import Bullet
from Utils import *

pygame.init()

player = Player()

bullets = []
enemies = []
score = 0

spawn_locations = [ # position des spawns possible pour les enemis a la moitié du terrain au 4 points cardinaux du terrain
    (0,(GRID_WIDTH//2)*TILE_SIZE),
    ((GRID_HEIGHT//2)*TILE_SIZE,0),
    (GRID_HEIGHT*TILE_SIZE,(GRID_WIDTH//2)*TILE_SIZE),
    ((GRID_HEIGHT//2)*TILE_SIZE,GRID_WIDTH*TILE_SIZE),
]

def spawn_enemy():
    if random.random() < 0.02:
        rand_spawn_location:list = spawn_locations[random.randint(0,len(spawn_locations)-1)]
        enemies.append(Enemy(rand_spawn_location[0], rand_spawn_location[1]))

def draw_map():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    (100,100,100),
                    (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

def draw_elements():
    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

def draw_score():
    score_text = small_font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))

def draw_game_over():
    text1 = font.render("GAME OVER", True, (255, 50, 50))
    text2 = small_font.render("F to Restart", True, (255,255,255))
    text3 = small_font.render("G to Quit", True, (255,255,255))

    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 40))
    
def reset_game():
    global player, bullets, enemies, score, game_state
    
    player = Player()
    bullets = []
    enemies = []
    score = 0
    game_state = "PLAYING"

game_state = "PLAYING"   # PLAYING / GAME_OVER
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)
running = True

while running:
    clock.tick(60)
    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "PLAYING":
                if event.key == pygame.K_f:
                    player.shoot(bullets)

                if event.key == pygame.K_g:
                    player.radial_shot(bullets)

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_f:
                    reset_game()
                if event.key == pygame.K_g:
                    running = False

    if game_state == "PLAYING":

        keys = pygame.key.get_pressed()
        player.move(keys, grid)

        spawn_enemy()

        # Update enemies
        for enemy in enemies[:]:
            enemy.update(player, enemies)

            distance = ((enemy.x - player.x)**2 + (enemy.y - player.y)**2)**0.5
            if distance < player.radius + enemy.radius:
                game_state = "GAME_OVER"

            for bullet in bullets[:]:
                dist = ((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2)**0.5
                if dist < enemy.radius:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.is_dead():
                bullets.remove(bullet)

        draw_map()
        draw_elements()
        draw_score()

    elif game_state == "GAME_OVER":
        draw_map()
        draw_elements()
        draw_score()
        draw_game_over()

    pygame.display.flip()

pygame.quit()