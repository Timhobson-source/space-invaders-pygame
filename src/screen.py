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
        self.screen_object_factory = ScreenObjectFactory(self)
        self.screen = screen
        self.game_meta = GameMeta()

    def update_screen_state(self):
        if self.player_has_lost():
            self.game_meta.stop_game()
            self.draw_losing_screen()
        else:
            self.update_and_draw_objects()

        pygame.display.update()

    def player_has_lost(self):
        if self.game_meta.game_being_played:
            max_y = self.screen.get_height(
            ) - config['window']['bottom_vertical_buffer']
            enemies_land = any(
                [
                    obj for obj in self.screen_objects
                    if isinstance(obj, Enemy) and obj.y >= max_y]
            )
            return (not self.game_meta.player_has_lives) or enemies_land
        return True

    def clear_objects_from_screen(self):
        self.screen_objects = []

    def draw_losing_screen(self):
        self.screen.fill(BG_COLOR)
        self.clear_objects_from_screen()
        box = self.screen_object_factory.create_lost_game_box(150, 200)
        box.draw(self.game_meta.points)

    def update_and_draw_objects(self):
        self.cleanup_off_screen_objects()
        self.handle_player_and_enemy_bullet_collisions()
        self.handle_enemy_and_player_bullet_collisions()

        self.screen.fill(BG_COLOR)
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
                    # TODO - add playing a "losing life" sound here
                    # and temporary color change for player object
                    self.game_meta.lose_life()
                    self.remove_screen_object(bullet)

    def register_screen_object(self, object):
        self.screen_objects.append(object)

    def remove_screen_object(self, object):
        self.screen_objects.remove(object)
