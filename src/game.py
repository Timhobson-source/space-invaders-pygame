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
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.25)

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

        self.game_meta = GameMeta(**self.config['meta'])
        screen_handler = ScreenHandler(window, self.game_meta)
        self.prepare_screen(screen_handler)

        running = True
        while running:
            pygame.time.delay(50)

            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                running = False

            if self.player_has_lost(screen_handler):
                self.game_meta.set_game_lost()
                pygame.mixer.music.fadeout(5000)
                self.draw_end_screen(screen_handler, 'YOU LOST!')
            elif self.player_has_won(screen_handler):
                self.game_meta.set_game_won()
                pygame.mixer.music.fadeout(5000)
                self.draw_end_screen(screen_handler, 'YOU WON!')
            else:
                screen_handler.update_screen_state()

            pygame.display.update()

            self.clock.tick(self.config['window']['fps'])

        pygame.quit()

    def player_has_lost(self, screen_handler):
        if self.game_meta.game_being_played:
            enemies_landed = any(screen_handler.enemies_landed)
            return (not self.game_meta.player_has_lives()) or enemies_landed
        return self.game_meta.lost_state

    def player_has_won(self, screen_handler):
        if self.game_meta.game_being_played:
            enemies_defeated = not screen_handler.enemies
            return self.game_meta.player_has_lives and enemies_defeated
        return self.game_meta.won_state

    def draw_end_screen(self, screen_handler, msg: str):
        screen_handler.screen.blit(screen_handler.bg, (0, 0))
        screen_handler.clear_objects_from_screen()
        box = screen_handler.screen_object_factory.create_end_game_box(msg)
        box.draw(self.game_meta.points)
