
class GameMeta:
    def __init__(self, start_lives=3, start_points=0):
        self.lives = start_lives
        self.points = start_points
        self.game_being_played = True
        self.lost_state = False
        self.won_state = False

    def lose_life(self):
        self.lives -= 1

    def increase_points(self, increase):
        self.points += increase

    def lose_points(self, decrease):
        if self.points < decrease:
            self.points = 0
        else:
            self.points -= decrease

    def player_has_lives(self):
        return self.lives > 0

    def stop_game(self):
        if self.game_being_played:
            self.game_being_played = False

    def set_game_lost(self):
        self.stop_game()
        self.lost_state = True
        self.won_state = False

    def set_game_won(self):
        self.stop_game()
        self.lost_state = False
        self.won_state = True
