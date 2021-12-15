import pygame

from config import get_config
from src.screen import ScreenHandler

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    config = get_config()

    window = pygame.display.set_mode(
        (config['window']['width'], config['window']['height'])
    )
    pygame.display.set_caption("Game!")

    screen_handler = ScreenHandler(window)
    screen_handler.create_score_box(420, 5, window)
    screen_handler.create_player(250, window.get_height() - 15, 25, 15, window)
    for i in range(6):
        screen_handler.create_enemy(100 + i*50, 200, 25, 10, window)

    running = True
    while running:
        pygame.time.delay(50)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False

        screen_handler.update_screen_state()

    pygame.quit()
    print('Thanks for playing!')
