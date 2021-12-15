from typing import List

import pygame

from src.screen_objects import Bullet, ScreenObject, BLACK

BG_COLOR = BLACK


class ScreenHandler:
    def __init__(self, screen: pygame.Surface, screen_objects: List[ScreenObject]):
        self.screen_objects = screen_objects
        self.screen = screen

    def update_screen_state(self):
        self.cleanup_off_screen_objects()
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

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)
