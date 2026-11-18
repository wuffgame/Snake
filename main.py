import random
import pygame


block_x = False
block_y = False

pygame.init()
window = pygame.display.set_mode((800, 800))
window.fill((0, 0, 0))
pygame.display.set_caption("Snake")

background_map = pygame.image.load("img/map.png").convert()

grid_size = 32

player = pygame.image.load("img/snake_front.png").convert_alpha()
player = pygame.transform.scale(player, (grid_size, grid_size))

player_x = 384
player_y = 384

dx = 0
dy = 0

eat_object = pygame.image.load("img/orange.png").convert_alpha()
eat_object = pygame.transform.scale(eat_object, (grid_size, grid_size))

def spawn_food():
    x = random.randint(1, 23) * grid_size
    y = random.randint(1, 23) * grid_size
    return x, y
eat_object_x, eat_object_y = spawn_food()


move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 150)

clock = pygame.time.Clock()

while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == move_event:
            player_x += dx
            player_y += dy

            if player_x == eat_object_x and player_y == eat_object_y:
                print("EAT EAT EAT!!!")
                eat_object_x, eat_object_y = spawn_food()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and block_x == False:
                dx = -grid_size
                dy = 0
                block_x = True
                block_y = False
            if event.key == pygame.K_RIGHT and block_x == False:
                dx = grid_size
                dy = 0
                block_x = True
                block_y = False
            if event.key == pygame.K_UP and block_y == False:
                dx = 0
                dy = -grid_size
                block_x = False
                block_y = True
            if event.key == pygame.K_DOWN and block_y == False:
                dx = 0
                dy = grid_size
                block_x = False
                block_y = True
            if event.key == pygame.K_a and block_x == False:
                dx = -grid_size
                dy = 0
                block_x = True
                block_y = False
            if event.key == pygame.K_d and block_x == False:
                dx = grid_size
                dy = 0
                block_x = True
                block_y = False
            if event.key == pygame.K_w and block_y == False:
                dx = 0
                dy = -grid_size
                block_x = False
                block_y = True
            if event.key == pygame.K_s and block_y == False:
                dx = 0
                dy = grid_size
                block_x = False
                block_y = True

# window border
    if player_x < 0:
        player_x = 0
    elif player_x >= 800:
        player_x = 800 - grid_size

    if player_y < 0:
        player_y = 0
    elif player_y >= 800:
        player_y = 800 - grid_size

# end game
    if player_x < 32:
        print("end")
        quit(0)
    elif player_x >= 768:
        print("end")
        quit(0)

    if player_y < 32:
        print("end")
        quit(0)
    elif player_y >= 768:
        print("end")
        quit(0)


    #output
    window.fill((0, 0, 0))

    window.blit(background_map, (0, 0))
    window.blit(eat_object, (eat_object_x, eat_object_y))
    window.blit(player, (player_x, player_y))

    pygame.display.flip()

    clock.tick(60)

