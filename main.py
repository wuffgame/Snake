import pygame

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame. display.set_caption("Randomize snake")

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    window.fill((255, 255, 255))

    pygame.display.flip()

