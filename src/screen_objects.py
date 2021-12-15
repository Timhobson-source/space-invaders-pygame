from abc import ABC, abstractmethod
import time

import pygame

from config import get_config
from src.helpers import clip_value

config = get_config()

# Colours in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (102, 0, 102)

SHOOTING_RECOIL_TIME = 0.3  # seconds

DEFAULT_FONT = pygame.font.get_default_font()


class ScreenObjectFactory:
    def __init__(self):
        self.id_counter = 0

    def create(self, screen_object_cls, *args, **kwargs):
        self.id_counter += 1
        return screen_object_cls(*args, id=self.id_counter, **kwargs)


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
        # remove y move for now
        # if keys[pygame.K_UP]:
        #     self.y -= self.vel
        # if keys[pygame.K_DOWN]:
        #     self.y += self.vel
        if keys[pygame.K_SPACE]:
            self.shoot(screen_handler)

        # stop circle going out of the screen
        min_x = self.radius + config['window']['left_horizontal_buffer']
        max_x = self.window.get_width() - self.radius - \
            config['window']['right_horizontal_buffer']
        self.x = clip_value(self.x, min_x, max_x)

    def shoot(self, screen_handler, bullet_speed=None, bullet_radius=None):
        if bullet_speed is None:
            bullet_speed = config['bullet']['speed']
        if bullet_radius is None:
            bullet_radius = config['bullet']['radius']

        cur_time = time.time()
        if not self.last_bullet_time or cur_time - self.last_bullet_time > SHOOTING_RECOIL_TIME:
            self.last_bullet_time = cur_time

            # create a bullet object
            screen_handler.create_bullet(
                self.x, self.y, bullet_speed, bullet_radius, self.window)


class Enemy(Character):

    color: tuple = YELLOW
    label: str = 'X'
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        pass


class Bullet(Character):

    color: tuple = PURPLE
    label: str = ''
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        self.y -= self.vel

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
        # have screen_handler have access to the score?
        # whether as a direct attribute or through an attribute
        # which is a class for game meta information.
        # Then this method can update the text?
        # or just have it print the score in the draw method?
        pass

    def draw(self):
        score = 10
        lives = 3
        score_box = pygame.font.SysFont(self.font, self.size).render(
            f"Score: {score}", True, self.color
        )
        lives_box = pygame.font.SysFont(self.font, self.size).render(
            f"Lives: {lives}", True, self.color
        )
        self.window.blit(score_box, (self.x, self.y))
        self.window.blit(lives_box, (self.x, self.y + self.size))
