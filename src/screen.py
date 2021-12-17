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
    BLACK,
)

config = get_config()
BG_COLOR = BLACK  # TODO - make a more interesting background

EXPLOSION_SOUND = pygame.mixer.Sound('data/sounds/explosion.wav')


class ScreenHandler:
    def __init__(self, screen: pygame.Surface):
        self.screen_objects = []
        self.formations = []
        self.screen_object_factory = ScreenObjectFactory(self)
        self.screen = screen
        self.game_meta = GameMeta()

    def update_screen_state(self):
        self.cleanup_off_screen_objects()
        self.handle_player_and_enemy_bullet_collisions()
        self.handle_enemy_and_player_bullet_collisions()

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
            for bullet in bullets:
                if detect_collision(enemy, bullet):
                    # play explosion sound for collision
                    pygame.mixer.Sound.play(EXPLOSION_SOUND)

                    # remove relevant objects from screen
                    self.remove_screen_object(enemy)
                    self.remove_screen_object(bullet)
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

    def register_formation(self, formation):
        self.formations.append(formation)

    def remove_formation(self, formation):
        self.formations.remove(formation)
