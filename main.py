import random
import pygame

ate_food = 0
block_x = False
block_y = False

pygame.init()
window = pygame.display.set_mode((800, 800))
window.fill((0, 0, 0))
pygame.display.set_caption("The most boring Snake")

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

background_map = pygame.image.load("img/map.png").convert()

grid_size = 32
total_cells = 25 * 25

player = pygame.image.load("img/snake_front.png").convert_alpha()
player = pygame.transform.scale(player, (grid_size, grid_size))

body = pygame.image.load("img/snake_back.png").convert_alpha()
body = pygame.transform.scale(body, (grid_size, grid_size))

player_x = 384
player_y = 384

snake_body = [(player_x, player_y)]
grow = False

dx = 0
dy = 0

eat_object = pygame.image.load("img/orange.png").convert_alpha()
eat_object = pygame.transform.scale(eat_object, (grid_size, grid_size))

def spawn_food():
    x = random.randint(1, 23) * grid_size
    y = random.randint(1, 23) * grid_size
    return x, y

def reset_vars():
    global ate_food, block_x, block_y, player_x, player_y, snake_body, grow, dx, dy, eat_object_x, eat_object_y
    ate_food = 0
    block_x = False
    block_y = False
    player_x = 384
    player_y = 384
    snake_body = [(player_x, player_y)]
    grow = False
    dx = 0
    dy = 0
    eat_object_x, eat_object_y = spawn_food()

def end_screen(text, color):
    retry_btn = pygame.Rect(240, 480, 140, 55)
    quit_btn = pygame.Rect(420, 480, 140, 55)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_btn.collidepoint(event.pos):
                    reset_vars()
                    return
                if quit_btn.collidepoint(event.pos):
                    quit(0)

        window.fill((0, 0, 0))
        window.blit(background_map, (0, 0))
        window.blit(eat_object, (eat_object_x, eat_object_y))
        for segment_x, segment_y in snake_body[1:]:
            window.blit(body, (segment_x, segment_y))

        score_surface = font.render(str(ate_food), True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(768, 6))
        window.blit(score_surface, score_rect)

        overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        window.blit(overlay, (0, 0))

        msg = big_font.render(text, True, color)
        score_msg = font.render(f"Score: {ate_food}", True, (255, 255, 255))

        window.blit(msg, msg.get_rect(center=(400, 350)))
        window.blit(score_msg, score_msg.get_rect(center=(400, 415)))

        retry_txt = font.render("Retry", True, (255, 255, 255))
        quit_txt = font.render("Quit", True, (255, 255, 255))

        window.blit(retry_txt, retry_txt.get_rect(center=retry_btn.center))
        window.blit(quit_txt, quit_txt.get_rect(center=quit_btn.center))

        pygame.display.flip()
        clock.tick(60)

eat_object_x, eat_object_y = spawn_food()
reset_vars()

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 150)

clock = pygame.time.Clock()

while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == move_event:
            if dx != 0 or dy != 0:
                player_x += dx
                player_y += dy

                snake_body.insert(0, (player_x, player_y))

                if grow:
                    grow = False
                else:
                    snake_body.pop()

                if (player_x, player_y) in snake_body[1:]:
                    end_screen("GAME OVER", (255, 70, 70))
                    continue

                if player_x == eat_object_x and player_y == eat_object_y:
                    ate_food += 1
                    grow = True
                    if len(snake_body) >= total_cells:
                        end_screen("YOU WIN!", (80, 255, 120))
                        continue
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

    #window border
    if player_x < 0:
        player_x = 0
    elif player_x >= 800:
        player_x = 800 - grid_size

    if player_y < 0:
        player_y = 0
    elif player_y >= 800:
        player_y = 800 - grid_size

    #end game
    if player_x < 32:
        end_screen("GAME OVER", (255, 70, 70))
        continue
    elif player_x >= 768:
        end_screen("GAME OVER", (255, 70, 70))
        continue

    if player_y < 32:
        end_screen("GAME OVER", (255, 70, 70))
        continue
    elif player_y >= 768:
        end_screen("GAME OVER", (255, 70, 70))
        continue


    #output
    window.fill((0, 0, 0))

    window.blit(background_map, (0, 0))
    window.blit(eat_object, (eat_object_x, eat_object_y))
    for segment_x, segment_y in snake_body[1:]:
        window.blit(body, (segment_x, segment_y))
    window.blit(player, (player_x, player_y))

    score_surface = font.render(str(ate_food), True, (255, 255, 255))
    score_rect = score_surface.get_rect(topright=(768, 6))
    window.blit(score_surface, score_rect)

    pygame.display.flip()

    clock.tick(60)

