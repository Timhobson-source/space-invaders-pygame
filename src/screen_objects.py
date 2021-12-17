from abc import ABC, abstractmethod
import time
import random

import pygame

from config import get_config
from src.helpers import clip_value, get_lead_enemy

config = get_config()

# TODO - move all constants into a constants file
# which handles font and sound inits?

# Colours in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (102, 0, 102)
GREEN = (0, 255, 0)

PLAYER_SHOOTING_RECOIL_TIME = config['player']['bullet']['recoil']  # seconds
ENEMY_SHOOTING_RECOIL_TIME = 3  # seconds
# TODO - ^Make this variable for different levels of difficulty

DEFAULT_FONT = pygame.font.get_default_font()

# Keep shoot sounds separate as likely will to change them to different
# sounds down the line
pygame.mixer.init()
PLAYER_SHOOT_SOUND = pygame.mixer.Sound("data/sounds/shoot-sound.wav")
ENEMY_SHOOT_SOUND = pygame.mixer.Sound("data/sounds/shoot-sound.wav")


class ScreenObjectFactory:
    def __init__(self, screen_handler):
        self.screen_handler = screen_handler
        self.id_counter = 0

    def create(self, screen_object_cls, *args, **kwargs):
        self.id_counter += 1
        return screen_object_cls(*args, id=self.id_counter, **kwargs)

    def create_player(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen_handler.screen]
        obj = self.create(Player, *args)
        self.screen_handler.register_screen_object(obj)

    def create_standard_enemy(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen_handler.screen]
        obj = self.create(StandardEnemy, *args)
        self.screen_handler.register_screen_object(obj)

    def create_shooting_enemy(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen_handler.screen]
        obj = self.create(ShootingEnemy, *args)
        self.screen_handler.register_screen_object(obj)

    def create_player_bullet(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen_handler.screen]
        obj = self.create(PlayerBullet, *args)
        self.screen_handler.register_screen_object(obj)

    def create_enemy_bullet(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen_handler.screen]
        obj = self.create(EnemyBullet, *args)
        self.screen_handler.register_screen_object(obj)

    def create_score_box(self, x: int, y: int):
        args = [x, y, self.screen_handler.screen]
        obj = self.create(ScoreBox, *args)
        self.screen_handler.register_screen_object(obj)


class ScreenObject(ABC):

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    def __eq__(self, obj):
        return super().__eq__(obj) and (obj.id == self.id)

    @abstractmethod
    def update_state(self, screen_handler):
        pass


class Character(ScreenObject):
    """Do not instantiate child classes directly. Use the ScreenObjectFactory class."""

    label: str = None
    label_rgb: tuple = None
    color: tuple = None

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface, id: int):
        super().__init__(id)
        self.x = x
        self.y = y
        self.vel = vel
        self.radius = radius
        self.window = window
        self.text = pygame.font.SysFont(DEFAULT_FONT, 20).render(
            self.label, True, self.label_rgb
        )

    @abstractmethod
    def update_state(self, screen_handler):
        pass

    def draw(self):
        # format and redraw window for updated state
        text_coords = (self.x - self.text.get_width()//2,
                       self.y - self.text.get_height()//2)

        pygame.draw.circle(self.window, self.color,
                           (self.x, self.y), self.radius)
        self.window.blit(self.text, text_coords)

    def is_offscreen(self):
        max_y = self.window.get_height(
        ) - config['window']['bottom_vertical_buffer']
        min_y = config['window']['top_vertical_buffer']

        max_x = self.window.get_width(
        ) - config['window']['right_horizontal_buffer']
        min_x = config['window']['left_horizontal_buffer']

        if self.y > max_y or self.y < min_y:
            return True
        if self.x > max_x or self.x < min_x:
            return True
        return False


class Player(Character):

    color: tuple = RED
    label: str = 'player'
    label_rgb: tuple = WHITE

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface, id: int):
        self.last_bullet_time = None
        super().__init__(x, y, vel, radius, window, id)

    def update_state(self, screen_handler):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_SPACE]:
            self.shoot(screen_handler)

        # stop circle going out of the screen
        min_x = self.radius + config['window']['left_horizontal_buffer']
        max_x = self.window.get_width() - self.radius - \
            config['window']['right_horizontal_buffer']
        self.x = clip_value(self.x, min_x, max_x)

    def shoot(self, screen_handler):
        # TODO - move this into init?
        bullet_speed = config['player']['bullet']['speed']
        bullet_radius = config['player']['bullet']['radius']

        cur_time = time.time()
        if not self.last_bullet_time or (
                cur_time - self.last_bullet_time > PLAYER_SHOOTING_RECOIL_TIME):

            # play shooting sound effect
            pygame.mixer.Sound.play(PLAYER_SHOOT_SOUND)

            self.last_bullet_time = cur_time

            # create a bullet object
            screen_handler.screen_object_factory.create_player_bullet(
                self.x, self.y, bullet_speed, bullet_radius)


class Enemy(Character):
    """Trivial class for all enemies to inherit from."""

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface, id: int):
        self.direction = 1
        self.lead_enemy = None
        super().__init__(x, y, vel, radius, window, id)

    def update_state(self, screen_handler):
        enemies = [
            e for e in screen_handler.screen_objects if isinstance(e, Enemy)
        ]
        lead_enemy = get_lead_enemy(self.direction, enemies)
        del enemies  # avoid memory leak

        max_x = screen_handler.screen.get_width(
        ) - config['window']['right_horizontal_buffer'] - lead_enemy.radius
        min_x = config['window']['left_horizontal_buffer'] + lead_enemy.radius

        if self.direction > 0 and lead_enemy.x > max_x:
            self.direction = -1  # switch direction
            self.y += 4 * self.vel  # move downwards
        elif self.direction < 0 and lead_enemy.x < min_x:
            self.direction = 1  # switch direction
            self.y += 4 * self.vel  # move downwards

        self.x += self.direction * self.vel


class StandardEnemy(Enemy):

    color: tuple = YELLOW
    label: str = 'X'
    label_rgb: tuple = BLACK
    point_value = config['enemy']['standard_point_value']


class ShootingEnemy(Enemy):

    color: tuple = GREEN
    label: str = 'X'
    label_rgb: tuple = BLACK
    point_value = config['enemy']['shooter_point_value']
    shooting_freq = config['enemy']['shooting_frequency']

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface, id: int):
        self.last_bullet_time = time.time()
        super().__init__(x, y, vel, radius, window, id)

    def update_state(self, screen_handler):
        super().update_state(screen_handler)
        cur_time = time.time()
        if cur_time - self.last_bullet_time > ENEMY_SHOOTING_RECOIL_TIME:
            if random.random() < self.shooting_freq:
                self.shoot(screen_handler)
            self.last_bullet_time = cur_time

    def shoot(self, screen_handler):
        # TODO - move this into init?
        bullet_speed = config['enemy']['bullet']['speed']
        bullet_radius = config['enemy']['bullet']['radius']

        # play shooting sound effect
        pygame.mixer.Sound.play(ENEMY_SHOOT_SOUND)

        # create a bullet object
        screen_handler.screen_object_factory.create_enemy_bullet(
            self.x, self.y, bullet_speed, bullet_radius)


class PlayerBullet(Character):

    color: tuple = PURPLE
    label: str = ''
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        self.y -= self.vel


class EnemyBullet(Character):

    color: tuple = WHITE
    label: str = ''
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        self.y += self.vel


class ScoreBox(ScreenObject):

    font = DEFAULT_FONT
    size = 25
    color = WHITE

    def __init__(self, x: int, y: int, window: pygame.Surface, id: int):
        super().__init__(id)
        self.window = window
        self.x = x
        self.y = y

    def update_state(self, screen_handler):
        self.score = screen_handler.game_meta.points
        self.lives = screen_handler.game_meta.lives

    def draw(self):
        score_box = pygame.font.SysFont(self.font, self.size).render(
            f"Score: {self.score}", True, self.color
        )
        lives_box = pygame.font.SysFont(self.font, self.size).render(
            f"Lives: {self.lives}", True, self.color
        )
        self.window.blit(score_box, (self.x, self.y))
        self.window.blit(lives_box, (self.x, self.y + self.size))
