import pygame

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

dx = grid_size
dy = 0

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -grid_size
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = grid_size
                dy = 0
            if event.key == pygame.K_UP:
                dx = 0
                dy = -grid_size
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = grid_size
            if event.key == pygame.K_a:
                dx = -grid_size
                dy = 0
            if event.key == pygame.K_d:
                dx = grid_size
                dy = 0
            if event.key == pygame.K_w:
                dx = 0
                dy = -grid_size
            if event.key == pygame.K_s:
                dx = 0
                dy = grid_size

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
    window.blit(player, (player_x, player_y))

    pygame.display.flip()

    clock.tick(60)

