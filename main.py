import pygame

pygame.init()
window = pygame.display.set_mode((800, 800))
window.fill((0, 0, 0))
pygame.display.set_caption("Randomize snake")

background_map = pygame.image.load("img/map.png").convert()

grid_size = 32

player = pygame.image.load("img/snake_front.png").convert_alpha()
player = pygame.transform.scale(player, (grid_size, grid_size))

player_x = 0
player_y = 0

falling_object = pygame.surface.Surface((50, 50))
falling_object.fill((255, 255, 255))
falling_object = pygame.image.load("img/orange.png").convert_alpha()
falling_object = pygame.transform.scale(falling_object, (30, 30))

while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= grid_size
            if event.key == pygame.K_RIGHT:
                player_x += grid_size
            if event.key == pygame.K_UP:
                player_y -= grid_size
            if event.key == pygame.K_DOWN:
                player_y += grid_size


    #output
    window.fill((0, 0, 0))

    window.blit(background_map, (0, 0))
    window.blit(player, (player_x, player_y))

    pygame.display.flip()

