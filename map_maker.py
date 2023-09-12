import json
import pygame


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YEllOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
PURPLE = (255, 0, 255)
PINK = (255, 192, 203)

file_name = input("Enter the name of the file to save to: ")

pygame.init()
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Map Maker")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

player_pos = [0, 0]

rects = []
colors = []


def find_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def save_json(rects, file_name):
    with open("maps/" + file_name + ".json", 'w') as f:
        json.dump(rects, f)


def draw_rect(start, color):
    if start:
        # Draw rectangle from start to current mouse position
        pygame.draw.rect(screen, color, (
            start[0], start[1], pygame.mouse.get_pos()[0] - start[0], pygame.mouse.get_pos()[1] - start[1]), 1)


def draw_rects(rects, colors):
    for i in range(len(rects)):
        pygame.draw.rect(screen, colors[i], rects[i], 1)


def inputs(start, color):
    if pygame.mouse.get_pressed()[0]:
        if pygame.key.get_pressed()[pygame.K_p]:
            # Add player position
            player_pos[0] = pygame.mouse.get_pos()[0]
            player_pos[1] = pygame.mouse.get_pos()[1]
        if start and find_distance(start[0], start[1], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) > 10:
            end = pygame.mouse.get_pos()
            rects.append((start[0], start[1], end[0] - start[0], end[1] - start[1]))
            colors.append(color)
            start = None
        elif pygame.key.get_pressed()[pygame.K_s]:
            start = pygame.mouse.get_pos()
        elif pygame.key.get_pressed()[pygame.K_d]:
            start = None
            for rect in rects:
                if rect[0] < pygame.mouse.get_pos()[0] < rect[0] + rect[2] and rect[1] < pygame.mouse.get_pos()[1] < \
                        rect[1] + rect[3]:
                    colors.remove(colors[rects.index(rect)])
                    rects.remove(rect)
                    break
    return start


start = None

color = WHITE

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        # Select Color with number 1 - 9
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                color = BLACK
            if event.key == pygame.K_2:
                color = WHITE
            if event.key == pygame.K_3:
                color = RED
            if event.key == pygame.K_4:
                color = GREEN
            if event.key == pygame.K_5:
                color = BLUE
            if event.key == pygame.K_6:
                color = YEllOW
            if event.key == pygame.K_7:
                color = ORANGE
            if event.key == pygame.K_8:
                color = BROWN
            if event.key == pygame.K_9:
                color = PURPLE
            if event.key == pygame.K_0:
                color = PINK
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_RETURN:
                # convert tuples to lists
                file = [list(rects[i]) + list(colors[i]) for i in range(len(rects))]
                file.insert(0, player_pos)
                save_json(file, file_name)
                done = True
    screen.fill(BLACK)

    # Display color
    pygame.draw.rect(screen, color, (0, 0, 50, 50))

    start = inputs(start, color)

    pygame.draw.circle(screen, RED, player_pos, 5)

    draw_rect(start, color)

    draw_rects(rects, colors)

    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
