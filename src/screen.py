import os

import pygame

from config import get_config
from src.game_meta import GameMeta
from src.helpers import detect_collision
from src.screen_objects import (
    Player,
    PlayerBullet,
    EnemyBullet,
    Enemy,
    ScreenObjectFactory,
)

config = get_config()
BG = pygame.transform.scale(
    pygame.image.load(os.path.join('data', 'images', 'background.jpg')),
    (config['window']['width'], config['window']['height'])
)

EXPLOSION_SOUND = pygame.mixer.Sound('data/sounds/explosion.wav')
EXPLOSION_SOUND.set_volume(0.2)
HURT_SOUND = pygame.mixer.Sound('data/sounds/beep.wav')
HURT_SOUND.set_volume(4)


class ScreenHandler:
    bg = BG

    def __init__(self, screen: pygame.Surface, game_meta: GameMeta):
        self.screen_objects = []
        self.screen_object_factory = ScreenObjectFactory(self)
        self.screen = screen
        self.game_meta = game_meta

    def update_screen_state(self):
        self.cleanup_off_screen_objects()
        self.handle_player_and_enemy_bullet_collisions()
        self.handle_enemy_and_player_bullet_collisions()

        self.screen.blit(self.bg, (0, 0))
        for object in self.screen_objects:
            object.update_state(self)
            object.draw()

    def clear_objects_from_screen(self):
        self.screen_objects = []

    def cleanup_off_screen_objects(self):
        offscreen_objects = [
            object for object in self.screen_objects
            if isinstance(object, (PlayerBullet, EnemyBullet)) and object.is_offscreen()
        ]
        for object in offscreen_objects:
            self.remove_screen_object(object)

    def handle_enemy_and_player_bullet_collisions(self):
        bullets = [
            obj for obj in self.screen_objects if isinstance(obj, PlayerBullet)]
        enemies = [
            obj for obj in self.screen_objects if isinstance(obj, Enemy)]

        # check if any bullets are inside any enemy hitboxes
        for enemy in enemies:
            # get enemy centre and radius
            # find any bullet closer to centre than radius
            # and remove bullet and enemy from screen
            removed_bullets = []
            for bullet in bullets:
                if detect_collision(enemy, bullet):
                    # play explosion sound for collision
                    pygame.mixer.Sound.play(EXPLOSION_SOUND)

                    # remove relevant objects from screen
                    self.remove_screen_object(enemy)
                    if bullet not in removed_bullets:
                        self.remove_screen_object(bullet)
                        removed_bullets.append(bullet)
                    self.game_meta.increase_points(
                        enemy.point_value
                    )

    def handle_player_and_enemy_bullet_collisions(self):
        enemy_bullets = [
            obj for obj in self.screen_objects if isinstance(obj, EnemyBullet)]

        # expecting only one player but in case we decide to add multiplayer
        # keep the logic for handling multiple players at once
        players = [
            obj for obj in self.screen_objects if isinstance(obj, Player)]

        for player in players:
            for bullet in enemy_bullets:
                if detect_collision(player, bullet):
                    pygame.mixer.Sound.play(HURT_SOUND)
                    # TODO - add temporary color change for player object
                    self.game_meta.lose_life()
                    self.game_meta.lose_points(50)
                    self.remove_screen_object(bullet)

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)

    @property
    def enemies_landed(self):
        min_y_to_land = self.screen.get_height() - config['window']['bottom_buffer']
        enemies_landed = [
            obj for obj in self.screen_objects
            if isinstance(obj, Enemy)
            if obj.y > min_y_to_land
        ]
        return enemies_landed

    @property
    def enemies(self):
        return [obj for obj in self.screen_objects if isinstance(obj, Enemy)]
