import pygame

from config import get_config
from src.game_meta import GameMeta

from src.screen import ScreenHandler
from src.formations import build_enemy_formation


class Game:
    def __init__(self, fps=60):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.config = get_config()
        pygame.mixer.music.load('data/sounds/main_music.mp3')
        pygame.mixer.music.play()

    def create_screen(self):
        window = pygame.display.set_mode(
            (self.config['window']['width'], self.config['window']['height'])
        )
        pygame.display.set_caption("Game!")
        return window

    def prepare_screen(self, screen_handler: ScreenHandler):
        self.build_score_box(screen_handler)
        self.build_player(screen_handler)
        self.build_enemy_formation(screen_handler)

    def build_score_box(self, screen_handler: ScreenHandler):
        screen_handler.screen_object_factory.create_score_box(**self.config['scorebox'])

    def build_enemy_formation(self, screen_handler: ScreenHandler):
        # TODO - put the formation logic here now?
        build_enemy_formation(screen_handler, **self.config)

    def build_player(self, screen_handler: ScreenHandler):
        height = screen_handler.screen.get_height()
        bottom_buffer = self.config['window']['bottom_buffer']

        player_radius = self.config['player']['radius']
        player_x = screen_handler.screen.get_width() // 2
        player_y = height - bottom_buffer - player_radius
        player_vel = self.config['player']['vel']

        screen_handler.screen_object_factory.create_player(
            player_x,
            player_y,
            player_vel,
            player_radius
        )

    def play(self):
        window = self.create_screen()

        game_meta = GameMeta(**self.config['meta'])
        screen_handler = ScreenHandler(window, game_meta)
        self.prepare_screen(screen_handler)

        running = True
        while running:
            pygame.time.delay(50)

            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                running = False

            screen_handler.update_screen_state()
            self.clock.tick(self.config['window']['fps'])

        pygame.quit()
