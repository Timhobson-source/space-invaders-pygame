import math

import pygame

from config import get_config
from src.game_meta import GameMeta
from src.screen_objects import (
    Player,
    PlayerBullet,
    EnemyBullet,
    Enemy,
    ShootingEnemy,
    StandardEnemy,
    ScoreBox,
    ScreenObjectFactory,
    BLACK,
)

config = get_config()
BG_COLOR = BLACK

EXPLOSION_SOUND = pygame.mixer.Sound('data/sounds/explosion.wav')


class ScreenHandler:
    def __init__(self, screen: pygame.Surface):
        self.screen_objects = []
        self.screen_object_factory = ScreenObjectFactory()
        self.screen = screen
        self.game_meta = GameMeta()

    def update_screen_state(self):
        self.handle_player_enemy_bullet_collisions()
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
            if isinstance(object, (PlayerBullet, EnemyBullet)) and object.is_offscreen()
        ]
        for object in offscreen_objects:
            self.remove_screen_object(object)

    def cleanup_destroyed_enemies(self):
        bullets = [
            obj for obj in self.screen_objects if isinstance(obj, PlayerBullet)]
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
                    # play explosion sound for collision
                    pygame.mixer.Sound.play(EXPLOSION_SOUND)

                    # remove relevant objects from screen
                    self.remove_screen_object(enemy)
                    self.remove_screen_object(bullet)
                    self.game_meta.increase_points(
                        enemy.point_value
                    )

    def handle_player_enemy_bullet_collisions(self):
        enemy_bullets = [
            obj for obj in self.screen_objects if isinstance(obj, EnemyBullet)]

        # expecting only one player but in case we decide to add multiplayer
        # keep the logic for handling multiple players at once
        players = [
            obj for obj in self.screen_objects if isinstance(obj, Player)]

        for player in players:
            for bullet in enemy_bullets:
                dist = math.sqrt(
                    (player.x - bullet.x)**2 + (player.y - bullet.y)**2
                )
                if dist < player.radius + bullet.radius:
                    # more logic here needed if we add multiplayer
                    # as well as in GameMeta object.
                    # IDEA: use a dict of player -> lives/points mapping?

                    # TODO - add playing a "losing life" sound here
                    # and temporary color change for player object
                    self.game_meta.lose_life()
                    self.remove_screen_object(bullet)

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)

    def create_player(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen]
        obj = self.screen_object_factory.create(Player, *args)
        self.screen_objects.append(obj)

    def create_standard_enemy(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen]
        obj = self.screen_object_factory.create(StandardEnemy, *args)
        self.screen_objects.append(obj)

    def create_shooting_enemy(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen]
        obj = self.screen_object_factory.create(ShootingEnemy, *args)
        self.screen_objects.append(obj)

    def create_player_bullet(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen]
        obj = self.screen_object_factory.create(PlayerBullet, *args)
        self.screen_objects.append(obj)

    def create_enemy_bullet(self, x: int, y: int, vel: int, radius: int):
        args = [x, y, vel, radius, self.screen]
        obj = self.screen_object_factory.create(EnemyBullet, *args)
        self.screen_objects.append(obj)

    def create_score_box(self, x: int, y: int):
        args = [x, y, self.screen]
        obj = self.screen_object_factory.create(ScoreBox, *args)
        self.screen_objects.append(obj)
