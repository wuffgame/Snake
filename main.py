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
move_delay = 150

player_base = pygame.image.load("img/snake_front.png").convert_alpha()
player_base = pygame.transform.scale(player_base, (grid_size, grid_size))
player = player_base.copy()

body = pygame.image.load("img/snake_back.png").convert_alpha()
body = pygame.transform.scale(body, (grid_size, grid_size))

player_x = 384
player_y = 384

snake_body = [(player_x, player_y)]
prev_body = [(player_x, player_y)]
last_move_time = pygame.time.get_ticks()
grow = False

dx = 0
dy = 0

eat_object = pygame.image.load("img/orange.png").convert_alpha()
eat_object = pygame.transform.scale(eat_object, (grid_size, grid_size))

retries = 0

def set_head_angle(angle):
    global player
    player = pygame.transform.rotate(player_base, angle)

def spawn_food():
    x = random.randint(1, 23) * grid_size
    y = random.randint(1, 23) * grid_size
    return x, y

def lerp(a, b, t):
    return a + (b - a) * t

def reset_vars():
    global ate_food, block_x, block_y, player_x, player_y, snake_body, prev_body, last_move_time, grow, dx, dy, eat_object_x, eat_object_y, player
    ate_food = 0
    block_x = False
    block_y = False
    player_x = 384
    player_y = 384
    snake_body = [(player_x, player_y)]
    prev_body = [(player_x, player_y)]
    last_move_time = pygame.time.get_ticks()
    grow = False
    dx = 0
    dy = 0
    player = player_base.copy()
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
                    global retries
                    retries += 1
                    reset_vars()
                    return
                if quit_btn.collidepoint(event.pos):
                    quit(0)

        window.fill((0, 0, 0))
        window.blit(background_map, (0, 0))
        window.blit(eat_object, (eat_object_x, eat_object_y))
        for segment_x, segment_y in snake_body[1:]:
            window.blit(body, (segment_x, segment_y))
        window.blit(player, (player_x, player_y))

        score_surface = font.render(str(ate_food), True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(768, 6))
        window.blit(score_surface, score_rect)

        retries_surface = font.render(f"Retries: {retries}", True, (255, 255, 255))
        retries_rect = retries_surface.get_rect(topleft=(32, 6))
        window.blit(retries_surface, retries_rect)

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
pygame.time.set_timer(move_event, move_delay)

clock = pygame.time.Clock()

while True:
    now = pygame.time.get_ticks()

    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == move_event:
            last_move_time = now
            if dx != 0 or dy != 0:
                prev_body = list(snake_body)

                player_x += dx
                player_y += dy

                snake_body.insert(0, (player_x, player_y))

                if grow:
                    grow = False
                    prev_body.append(prev_body[-1])
                else:
                    snake_body.pop()

                while len(prev_body) < len(snake_body):
                    prev_body.append(prev_body[-1])
                prev_body = prev_body[:len(snake_body)]

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
            if event.key in (pygame.K_LEFT, pygame.K_a) and block_x == False:
                dx = -grid_size
                dy = 0
                block_x = True
                block_y = False
                set_head_angle(-90)
            if event.key in (pygame.K_RIGHT, pygame.K_d) and block_x == False:
                dx = grid_size
                dy = 0
                block_x = True
                block_y = False
                set_head_angle(90)
            if event.key in (pygame.K_UP, pygame.K_w) and block_y == False:
                dx = 0
                dy = -grid_size
                block_x = False
                block_y = True
                set_head_angle(180)
            if event.key in (pygame.K_DOWN, pygame.K_s) and block_y == False:
                dx = 0
                dy = grid_size
                block_x = False
                block_y = True
                set_head_angle(0)

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
    hit_border = False
    if player_x < 32:
        player_x = 32
        hit_border = True
    elif player_x >= 768:
        player_x = 768 - grid_size
        hit_border = True

    if player_y < 32:
        player_y = 32
        hit_border = True
    elif player_y >= 768:
        player_y = 768 - grid_size
        hit_border = True

    if hit_border:
        if snake_body:
            snake_body[0] = (player_x, player_y)
        end_screen("GAME OVER", (255, 70, 70))
        continue

    if dx == 0 and dy == 0:
        t = 1.0
    else:
        t = min(1.0, (now - last_move_time) / move_delay)

    #output
    window.fill((0, 0, 0))

    window.blit(background_map, (0, 0))
    window.blit(eat_object, (eat_object_x, eat_object_y))

    for i in range(1, len(snake_body)):
        px, py = prev_body[i]
        cx, cy = snake_body[i]
        window.blit(body, (lerp(px, cx, t), lerp(py, cy, t)))

    head_px, head_py = prev_body[0]
    head_cx, head_cy = snake_body[0]
    window.blit(player, (lerp(head_px, head_cx, t), lerp(head_py, head_cy, t)))

    score_surface = font.render(f"Points: {ate_food}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(topright=(768, 6))
    window.blit(score_surface, score_rect)

    retries_surface = font.render(f"Retries: {retries}", True, (255, 255, 255))
    retries_rect = retries_surface.get_rect(topleft=(32, 6))
    window.blit(retries_surface, retries_rect)

    pygame.display.flip()

    clock.tick(60)