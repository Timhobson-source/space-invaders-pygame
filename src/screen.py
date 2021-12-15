import math

import pygame

from src.screen_objects import (
    Player,
    Bullet,
    Enemy,
    ScreenObjectFactory,
    BLACK,
)

BG_COLOR = BLACK


class ScreenHandler:
    def __init__(self, screen: pygame.Surface):
        self.screen_objects = []
        self.screen_object_factory = ScreenObjectFactory()
        self.screen = screen

    def update_screen_state(self):
        self.cleanup_off_screen_objects()
        self.cleanup_destroyed_enemies()
        self.screen.fill(BG_COLOR)
        for object in self.screen_objects:
            object.update_state(self)
            object.draw()
        pygame.display.update()

    def cleanup_off_screen_objects(self):
        offscreen_objects = [
            object for object in self.screen_objects
            if isinstance(object, Bullet) and object.is_offscreen()
        ]
        for object in offscreen_objects:
            self.remove_screen_object(object)

    def cleanup_destroyed_enemies(self):
        bullets = [
            obj for obj in self.screen_objects if isinstance(obj, Bullet)]
        enemies = [
            obj for obj in self.screen_objects if isinstance(obj, Enemy)]

        # check if any bullets are inside any enemy hitboxes
        for enemy in enemies:
            # get enemy centre and radius
            # find any bullet closer to centre than radius
            # and remove bullet and enemy from screen
            for bullet in bullets:
                dist = math.sqrt(
                    (enemy.x - bullet.x)**2 +
                    (enemy.y - bullet.y)**2
                )
                if dist <= enemy.radius + bullet.radius:
                    self.remove_screen_object(enemy)
                    self.remove_screen_object(bullet)

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)

    def create_player(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface):
        args = [x, y, vel, radius, window]
        obj = self.screen_object_factory.create(Player, *args)
        self.screen_objects.append(obj)

    def create_enemy(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface):
        args = [x, y, vel, radius, window]
        obj = self.screen_object_factory.create(Enemy, *args)
        self.screen_objects.append(obj)

    def create_bullet(self, x: int, y: int, vel: int, radius: int, window: pygame.Surface):
        args = [x, y, vel, radius, window]
        obj = self.screen_object_factory.create(Bullet, *args)
        self.screen_objects.append(obj)
