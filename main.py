import pygame

from config import get_config
from src.screen import ScreenHandler
from src.helpers import generate_enemy_grid


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    config = get_config()

    window = pygame.display.set_mode(
        (config['window']['width'], config['window']['height'])
    )
    pygame.display.set_caption("Game!")

    screen_handler = ScreenHandler(window)
    screen_handler.create_score_box(**config['scorebox'])
    screen_handler.create_player(250, window.get_height(
    ) - 15 - config['window']['bottom_vertical_buffer'], 25, 15)
    generate_enemy_grid(screen_handler)

    running = True
    while running:
        pygame.time.delay(50)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False

        screen_handler.update_screen_state()

    pygame.quit()
    print('Thanks for playing!')
