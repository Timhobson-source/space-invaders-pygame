import pygame

from src.screen import ScreenHandler

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game!")

    screen_handler = ScreenHandler(window)
    screen_handler.create_player(250, window.get_height() - 15, 25, 15, window)
    screen_handler.create_enemy(100, 200, 25, 10, window)

    running = True
    while running:
        pygame.time.delay(50)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False

        screen_handler.update_screen_state()

    pygame.quit()
    print('Thanks for playing!')
