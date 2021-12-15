import pygame

from src.screen import ScreenHandler
from src.screen_objects import Enemy, Player

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game!")

    player = Player(250, 250, 25, 15, window)
    enemy = Enemy(100, 200, 25, 10, window)
    screen_objects = [player, enemy]

    screen_handler = ScreenHandler(window, screen_objects)

    running = True
    while running:
        pygame.time.delay(50)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False

        screen_handler.update_screen_state()

    pygame.quit()
    print('Thanks for playing!')
