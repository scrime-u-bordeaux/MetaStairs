import pygame

def init():
    global screen
    global font

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Meta Stairs Monitor')
    font = pygame.font.SysFont(None, 24)

def display_multiline_text(lines):
    x = 20
    y = 20
    screen.fill((0, 0, 0))
    for i, l in enumerate(lines):
        surface = font.render(l, True, (255, 255, 255))
        screen.blit(surface, (x, y + i * 30))
    pygame.display.flip()

def check_keyboard_events():
    res = []
    for event in pygame.event.get():
        if (event.type == pygame.KEYUP):
            keyName = pygame.key.name(event.key)
            res.append(keyName)
        elif (event.type == pygame.KEYDOWN):
            # keyName = pygame.key.name(event.key)
            pass
    return res