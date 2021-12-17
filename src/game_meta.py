
class GameMeta:
    def __init__(self, start_lives=3, start_points=0):
        self.lives = start_lives
        self.points = start_points
        self.game_being_played = True

    def lose_life(self):
        self.lives -= 1

    def increase_points(self, increase):
        self.points += increase

    def player_has_lives(self):
        return self.lives > 0

    def stop_game(self):
        if self.game_being_played:
            self.game_being_played = False
