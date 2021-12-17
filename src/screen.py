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


class ScreenHandler:
    def __init__(self, screen: pygame.Surface):
        self.screen_objects = []
        self.screen_object_factory = ScreenObjectFactory(self)
        self.screen = screen
        self.game_meta = GameMeta()

    def update_screen_state(self):
        if self.player_has_lost():
            self.game_meta.set_game_lost()
            self.draw_end_screen('YOU LOST!')
        elif self.player_has_won():
            self.game_meta.set_game_won()
            self.draw_end_screen('YOU WON!')
        else:
            self.update_and_draw_objects()

        pygame.display.update()

    def player_has_lost(self):
        if self.game_meta.game_being_played:
            max_y = self.screen.get_height(
            ) - config['window']['bottom_buffer']
            enemies_land = any(
                [
                    obj for obj in self.screen_objects
                    if isinstance(obj, Enemy) and obj.y >= max_y]
            )
            return (not self.game_meta.player_has_lives()) or enemies_land
        return self.game_meta.lost_state

    def player_has_won(self):
        if self.game_meta.game_being_played:
            enemies_defeated = not [obj for obj in self.screen_objects if isinstance(obj, Enemy)]
            return self.game_meta.player_has_lives and enemies_defeated
        return self.game_meta.won_state

    def clear_objects_from_screen(self):
        self.screen_objects = []

    def draw_end_screen(self, msg: str):
        self.screen.blit(BG, (0, 0))
        self.clear_objects_from_screen()
        box = self.screen_object_factory.create_end_game_box(150, 200, msg)
        box.draw(self.game_meta.points)

    def update_and_draw_objects(self):
        self.cleanup_off_screen_objects()
        self.handle_player_and_enemy_bullet_collisions()
        self.handle_enemy_and_player_bullet_collisions()

        self.screen.blit(BG, (0, 0))
        for object in self.screen_objects:
            object.update_state(self)
            object.draw()

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
                    # TODO - add playing a "losing life" sound here
                    # and temporary color change for player object
                    self.game_meta.lose_life()
                    self.remove_screen_object(bullet)

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)
