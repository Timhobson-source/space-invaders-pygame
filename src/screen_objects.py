from abc import ABC, abstractmethod
import time

import pygame

from src.helpers import clip_value

# Colours in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (102, 0, 102)

SHOOTING_RECOIL_TIME = 0.3  # seconds


class ScreenObject(ABC):

    label: str = None
    label_rgb: tuple = None
    color: tuple = None

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface):
        self.x = x
        self.y = y
        self.vel = vel
        self.radius = radius
        self.window = window
        font = pygame.font.get_default_font()
        self.text = pygame.font.SysFont(font, 20).render(
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


class Player(ScreenObject):

    color: tuple = RED
    label: str = 'player'
    label_rgb: tuple = WHITE

    def __init__(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface):
        self.last_bullet_time = None
        super().__init__(x, y, vel, radius, window)

    def update_state(self, screen_handler):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        if keys[pygame.K_SPACE]:
            self.shoot(screen_handler)

        # stop circle going out of the screen
        self.x = clip_value(self.x, self.radius,
                            self.window.get_width() - self.radius)
        self.y = clip_value(self.y, self.radius,
                            self.window.get_height() - self.radius)

    def shoot(self, screen_handler, bullet_speed=20, bullet_radius=5):
        cur_time = time.time()
        if not self.last_bullet_time or cur_time - self.last_bullet_time > SHOOTING_RECOIL_TIME:
            self.last_bullet_time = cur_time

            # create a bullet object
            bullet = Bullet(self.x, self.y, vel=bullet_speed,
                            radius=bullet_radius, window=self.window)

            # let screen handler know about bullet object
            screen_handler.register_screen_object(bullet)


class Enemy(ScreenObject):

    color: tuple = YELLOW
    label: str = 'X'
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        pass


class Bullet(ScreenObject):

    color: tuple = PURPLE
    label: str = ''
    label_rgb: tuple = BLACK

    def update_state(self, screen_handler):
        self.y -= self.vel

    def is_offscreen(self):
        if self.y > self.window.get_height() or self.y < 0:
            return True
        if self.x > self.window.get_width() or self.x < 0:
            return True
        return False
