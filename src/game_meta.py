

class GameMeta:
    def __init__(self, start_lives=3, start_points=0):
        self.lives = start_lives
        self.points = start_points

    def lose_life(self):
        self.lives -= 1

    def increase_points(self, increase):
        self.points += increase
