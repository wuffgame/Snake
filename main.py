import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Randomize snake")

player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))
player = pygame.image.load("img/snake_front.png").convert_alpha()
player = pygame.transform.scale(player, (40, 40))

player_x = 0
player_y = 0
player_vel_x = 0
player_vel_y = 0

falling_object = pygame.surface.Surface((50, 50))
falling_object.fill((255, 255, 255))
falling_object = pygame.image.load("img/orange.png").convert_alpha()
falling_object = pygame.transform.scale(falling_object, (30, 30))

falling_object_x = 0
falling_object_y = 0
falling_object_vel_x = 0
falling_object_vel_y = -.3

while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_vel_x = -0.2
                player_vel_y = 0
            if event.key == pygame.K_RIGHT:
                player_vel_x = 0.2
                player_vel_y = 0
            if event.key == pygame.K_DOWN:
                player_vel_y = 0.2
                player_vel_x = 0
            if event.key == pygame.K_UP:
                player_vel_y = -0.2
                player_vel_x = 0


    #output
    window.fill((0, 0, 0))

    player_x += player_vel_x
    player_y += player_vel_y
    window.blit(player, (player_x, player_y))
    falling_object_x += falling_object_vel_x
    falling_object_y += falling_object_y
    window.blit(falling_object, (falling_object_x, falling_object_y))

    pygame.display.flip()

