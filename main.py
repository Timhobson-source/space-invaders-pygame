import pygame

from config import get_config
from src.screen import ScreenHandler
from src.formations import build_formation


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    config = get_config()

    window = pygame.display.set_mode(
        (config['window']['width'], config['window']['height'])
    )
    pygame.display.set_caption("Game!")

    screen_handler = ScreenHandler(window)
    screen_handler.screen_object_factory.create_score_box(**config['scorebox'])
    screen_handler.screen_object_factory.create_player(250, window.get_height(
    ) - 15 - config['window']['bottom_vertical_buffer'], 25, 15)
    build_formation(screen_handler)

    running = True
    while running:
        pygame.time.delay(50)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            running = False

        screen_handler.update_screen_state()

    pygame.quit()
    print('Thanks for playing!')
