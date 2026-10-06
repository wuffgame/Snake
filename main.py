import pygame

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Randomize snake")

player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))

player_x = 0
player_y = 0
player_vel_x = 0
player_vel_y = 0

while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    #output
    window.fill((0, 0, 0))

    window.blit(player, (player_x, player_y))

    pygame.display.flip()

