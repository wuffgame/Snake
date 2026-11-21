import random
import sys
from pathlib import Path
import pygame


BASE_SIZE = 800
GRID_SIZE = 32
TOTAL_CELLS = 25 * 25
MOVE_DELAY = 150


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    elif getattr(sys, "frozen", False):
        base_path = Path(sys.executable).resolve().parent
    else:
        base_path = Path(__file__).resolve().parent
    return str(base_path / relative_path)


def exit_game():
    pygame.quit()
    sys.exit(0)


def compute_initial_window_size() -> tuple[int, int]:
    info = pygame.display.Info()
    max_w = max(480, int(info.current_w * 0.85)) if info.current_w > 0 else BASE_SIZE
    max_h = max(480, int(info.current_h * 0.85)) if info.current_h > 0 else BASE_SIZE
    size = min(BASE_SIZE, max_w, max_h)
    return size, size


pygame.init()
win_w, win_h = compute_initial_window_size()
window = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
canvas = pygame.Surface((BASE_SIZE, BASE_SIZE))
pygame.display.set_caption("The most boring Snake")

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

background_map = pygame.image.load(resource_path("img/map.png")).convert()
background_map = pygame.transform.smoothscale(background_map, (BASE_SIZE, BASE_SIZE))

player_base = pygame.image.load(resource_path("img/snake_front.png")).convert_alpha()
player_base = pygame.transform.scale(player_base, (GRID_SIZE, GRID_SIZE))
player = player_base.copy()

body = pygame.image.load(resource_path("img/snake_back.png")).convert_alpha()
body = pygame.transform.scale(body, (GRID_SIZE, GRID_SIZE))

eat_object = pygame.image.load(resource_path("img/orange.png")).convert_alpha()
eat_object = pygame.transform.scale(eat_object, (GRID_SIZE, GRID_SIZE))

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
eat_object_x = 0
eat_object_y = 0
retries = 0


def get_viewport_rect() -> pygame.Rect:
    cur_w, cur_h = window.get_size()
    scale = min(cur_w / BASE_SIZE, cur_h / BASE_SIZE)
    scaled_w = int(BASE_SIZE * scale)
    scaled_h = int(BASE_SIZE * scale)
    offset_x = (cur_w - scaled_w) // 2
    offset_y = (cur_h - scaled_h) // 2
    return pygame.Rect(offset_x, offset_y, scaled_w, scaled_h)


def window_to_canvas_pos(pos: tuple[int, int]) -> tuple[float, float] | None:
    rect = get_viewport_rect()
    if rect.width <= 0 or rect.height <= 0 or not rect.collidepoint(pos):
        return None
    vx = (pos[0] - rect.x) * (BASE_SIZE / rect.width)
    vy = (pos[1] - rect.y) * (BASE_SIZE / rect.height)
    return vx, vy


def present_canvas():
    window.fill((0, 0, 0))
    rect = get_viewport_rect()
    scaled_surf = pygame.transform.smoothscale(canvas, (rect.width, rect.height))
    window.blit(scaled_surf, rect.topleft)
    pygame.display.flip()


def handle_window_event(event: pygame.event.Event) -> bool:
    global window
    if event.type == pygame.QUIT:
        exit_game()
    if event.type == pygame.VIDEORESIZE:
        new_w = max(320, event.w)
        new_h = max(320, event.h)
        window = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
        return True
    return False


def set_head_angle(angle: float):
    global player
    player = pygame.transform.rotate(player_base, angle)


def spawn_food() -> tuple[int, int]:
    occupied = set(snake_body)
    while True:
        x = random.randint(1, 23) * GRID_SIZE
        y = random.randint(1, 23) * GRID_SIZE
        if (x, y) not in occupied:
            return x, y


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def reset_vars():
    global ate_food, block_x, block_y, player_x, player_y, snake_body, prev_body
    global last_move_time, grow, dx, dy, eat_object_x, eat_object_y, player
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


def end_screen(text: str, color: tuple[int, int, int]):
    global retries
    retry_btn = pygame.Rect(240, 480, 140, 55)
    quit_btn = pygame.Rect(420, 480, 140, 55)

    while True:
        for event in pygame.event.get():
            handle_window_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mapped = window_to_canvas_pos(event.pos)
                if mapped is not None:
                    if retry_btn.collidepoint(mapped):
                        retries += 1
                        reset_vars()
                        return
                    if quit_btn.collidepoint(mapped):
                        exit_game()

        canvas.fill((0, 0, 0))
        canvas.blit(background_map, (0, 0))
        canvas.blit(eat_object, (eat_object_x, eat_object_y))
        for segment_x, segment_y in snake_body[1:]:
            canvas.blit(body, (segment_x, segment_y))
        canvas.blit(player, (player_x, player_y))

        score_surface = font.render(str(ate_food), True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(768, 6))
        canvas.blit(score_surface, score_rect)

        retries_surface = font.render(f"Retries: {retries}", True, (255, 255, 255))
        retries_rect = retries_surface.get_rect(topleft=(32, 6))
        canvas.blit(retries_surface, retries_rect)

        overlay = pygame.Surface((BASE_SIZE, BASE_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        canvas.blit(overlay, (0, 0))

        msg = big_font.render(text, True, color)
        score_msg = font.render(f"Score: {ate_food}", True, (255, 255, 255))

        canvas.blit(msg, msg.get_rect(center=(400, 350)))
        canvas.blit(score_msg, score_msg.get_rect(center=(400, 415)))

        retry_txt = font.render("Retry", True, (255, 255, 255))
        quit_txt = font.render("Quit", True, (255, 255, 255))

        canvas.blit(retry_txt, retry_txt.get_rect(center=retry_btn.center))
        canvas.blit(quit_txt, quit_txt.get_rect(center=quit_btn.center))

        present_canvas()
        clock.tick(60)


reset_vars()

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, MOVE_DELAY)

clock = pygame.time.Clock()

while True:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        handle_window_event(event)

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
                prev_body = prev_body[: len(snake_body)]

                if (player_x, player_y) in snake_body[1:]:
                    end_screen("GAME OVER", (255, 70, 70))
                    continue

                if player_x == eat_object_x and player_y == eat_object_y:
                    ate_food += 1
                    grow = True
                    if len(snake_body) >= TOTAL_CELLS:
                        end_screen("YOU WIN!", (80, 255, 120))
                        continue
                    eat_object_x, eat_object_y = spawn_food()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a) and not block_x:
                dx = -GRID_SIZE
                dy = 0
                block_x = True
                block_y = False
                set_head_angle(-90)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and not block_x:
                dx = GRID_SIZE
                dy = 0
                block_x = True
                block_y = False
                set_head_angle(90)
            elif event.key in (pygame.K_UP, pygame.K_w) and not block_y:
                dx = 0
                dy = -GRID_SIZE
                block_x = False
                block_y = True
                set_head_angle(180)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and not block_y:
                dx = 0
                dy = GRID_SIZE
                block_x = False
                block_y = True
                set_head_angle(0)

    if player_x < 0:
        player_x = 0
    elif player_x >= BASE_SIZE:
        player_x = BASE_SIZE - GRID_SIZE

    if player_y < 0:
        player_y = 0
    elif player_y >= BASE_SIZE:
        player_y = BASE_SIZE - GRID_SIZE

    hit_border = False
    if player_x < 32:
        player_x = 32
        hit_border = True
    elif player_x >= 768:
        player_x = 768 - GRID_SIZE
        hit_border = True

    if player_y < 32:
        player_y = 32
        hit_border = True
    elif player_y >= 768:
        player_y = 768 - GRID_SIZE
        hit_border = True

    if hit_border:
        if snake_body:
            snake_body[0] = (player_x, player_y)
        end_screen("GAME OVER", (255, 70, 70))
        continue

    if dx == 0 and dy == 0:
        t = 1.0
    else:
        t = min(1.0, (now - last_move_time) / MOVE_DELAY)

    canvas.fill((0, 0, 0))
    canvas.blit(background_map, (0, 0))
    canvas.blit(eat_object, (eat_object_x, eat_object_y))

    for i in range(1, len(snake_body)):
        px, py = prev_body[i]
        cx, cy = snake_body[i]
        canvas.blit(body, (lerp(px, cx, t), lerp(py, cy, t)))

    head_px, head_py = prev_body[0]
    head_cx, head_cy = snake_body[0]
    canvas.blit(player, (lerp(head_px, head_cx, t), lerp(head_py, head_cy, t)))

    score_surface = font.render(f"Points: {ate_food}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(topright=(768, 6))
    canvas.blit(score_surface, score_rect)

    retries_surface = font.render(f"Retries: {retries}", True, (255, 255, 255))
    retries_rect = retries_surface.get_rect(topleft=(32, 6))
    canvas.blit(retries_surface, retries_rect)

    present_canvas()
    clock.tick(60)