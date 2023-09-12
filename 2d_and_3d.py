import sys

import pygame
import math
import json

WIDTH = 1440
HEIGHT = 720

WHITE = (255, 255, 255)


class Character:
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect(x, y, 30, 30)
        self.rect.x = x
        self.rect.y = y
        self.angle = 0

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


def draw_map(screen, map):
    rects = []
    colors = []
    for rect in map:
        new = pygame.draw.rect(screen, (rect[4], rect[5], rect[6]), [(rect[0], rect[1]), (rect[2], rect[3])])
        colors.append((rect[4], rect[5], rect[6]))
        rects.append(new)
    return rects, colors


def magnitude(center1, center2):
    x = center1[0] - center2[0]
    y = center1[1] - center2[1]
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))


def magnitude2(dx, dy):
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


def reset_angel(character):
    if 0 < character.angle:
        character.angle += 2 * math.pi
    if character.angle > 2 * math.pi:
        character.angle -= 2 * math.pi


def touching_side(character, rects):
    if character.rect.x < 5:
        return "left"
    if character.rect.x + character.rect.width > WIDTH / 2:
        return "right"
    for rect in rects:
        if rect.collidepoint(character.rect.x, character.rect.centery):
            return "left"
        if rect.collidepoint(character.rect.x + character.rect.width, character.rect.centery):
            return "right"


def touching_top_or_bottom(character, rects):
    if character.rect.y < 5:
        return "bottom"
    if character.rect.y + character.rect.height > HEIGHT:
        return "top"
    for rect in rects:
        if rect.collidepoint(character.rect.centerx, character.rect.y):
            return "bottom"
        if rect.collidepoint(character.rect.centerx, character.rect.y + character.rect.height):
            return "top"


def move(character, rects, angle=0.0):
    dx = 5 * math.cos(character.angle + angle)
    dy = 5 * math.sin(character.angle + angle)
    sidex = touching_side(character, rects)
    sidey = touching_top_or_bottom(character, rects)
    if (dx < 0 and sidex == "left") or (dx > 0 and sidex == "right"):
        dx = 0
    if (dy < 0 and sidey == "bottom") or (dy > 0 and sidey == "top"):
        dy = 0
    m = magnitude2(dx, dy)
    if m == 0:
        m = 1
    character.move(2 * dx / m, 2 * dy / m)


def move2(character, rects, angle=0.0):
    dx = math.cos(character.angle + angle)
    dy = math.sin(character.angle + angle)
    m = magnitude2(dx, dy)
    sidex = touching_side(character, rects)
    sidey = touching_top_or_bottom(character, rects)
    if (dx < 0 and sidex == "left") or (dx > 0 and sidex == "right"):
        dx = 0
    if (dy < 0 and sidey == "bottom") or (dy > 0 and sidey == "top"):
        dy = 0
    if m == 0:
        m = 100
    character.move(5 * dx / m, 5 * dy / m)


def keyboard_inputs(character, rects):
    """
    This function handles all keyboard inputs.
    If the user preseses the W key, the character will move forward.
    If the user preseses the A key, the character will rotate left.
    If the user preseses the S key, the character will move backward.
    If the user preseses the D key, the character will rotate right.
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        move2(character, rects, -math.pi / 2)
    if keys[pygame.K_d]:
        move2(character, rects, math.pi / 2)
    if keys[pygame.K_w]:
        move2(character, rects)
    if keys[pygame.K_s]:
        move2(character, rects, math.pi)

    if keys[pygame.K_q]:
        character.angle -= math.pi / 64
    if keys[pygame.K_e]:
        character.angle += math.pi / 64


def draw_vision(character, screen):
    x, y = character.rect.center
    new_x = x + 50 * math.cos(character.angle)
    new_y = y + 50 * math.sin(character.angle)
    pygame.draw.line(screen, (255, 0, 0), (x, y), (new_x, new_y), 5)


def in_bounds(x, y, width, height):
    if not (0 < x < width):
        return False
    if not (0 < y < height):
        return False
    return True


def touching(x, y, rects, colors):
    for i in range(len(rects)):
        if rects[i].collidepoint(x, y):
            return colors[i]
    return False


def find_endpoint(center, angle, rects, colors):
    x, y = center
    count = 0
    while in_bounds(x, y, WIDTH / 2, HEIGHT) and count < 180:
        color = touching(x, y, rects, colors)
        if color:
            return (x, y), color
        x += math.cos(angle)
        y += math.sin(angle)
        count += 1
    return (x, y), (255, 255, 255)


def draw_more_vision(character, screen, rects, colors):
    lengths = []
    new_colors = []
    angle = character.angle - math.pi / 4
    for i in range(80):
        endpoint, color = find_endpoint(character.rect.center, angle, rects, colors)
        new_colors.append(color)
        if endpoint:
            m = magnitude(character.rect.center, endpoint)
            if m == 0:
                m = 1
            lengths.append(HEIGHT / (0.1 * m))
            pygame.draw.line(screen, WHITE, character.rect.center, endpoint)
        else:
            lengths.append(None)
        angle += math.pi / 128
    return lengths, new_colors


def darken_color(color, amount):
    r, g, b = color
    r -= 10000 // amount
    g -= 10000 // amount
    b -= 10000 // amount
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    return r, g, b


def draw_3d(screen, lengths, colors):
    left_side = WIDTH // 2
    middle = HEIGHT // 2
    num_rects = len(lengths)
    rect_width = left_side / num_rects
    for i in range(num_rects):
        if lengths[i]:
            color = darken_color(colors[i], lengths[i])
            pygame.draw.rect(screen, color,
                             [(left_side + i * rect_width, middle - lengths[i]), (rect_width, 2 * lengths[i])])


def update_screen(screen, character, map):
    """
    This function updates the screen.
    The background is black.
    :param screen:
    :param background:
    :param character:
    :return:
    """
    screen.fill((0, 0, 0))
    rects, colors = draw_map(screen, map)
    keyboard_inputs(character, rects)
    reset_angel(character)
    draw_vision(character, screen)
    lengths, colors = draw_more_vision(character, screen, rects, colors)
    draw_3d(screen, lengths, colors)


def load_json(json_file):
    with open(json_file) as file:
        return json.load(file)


def main(file):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pygame Test")
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    map = load_json("maps/" + file)
    pos = map.pop(0)
    character = Character(pos[0], pos[1])
    while True:
        clock.tick(16)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                dx, dy = event.rel
                character.angle += dx / 500
        update_screen(screen, character, map)
        pygame.display.update()


if __name__ == "__main__":
    main(sys.argv[1])
