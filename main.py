from src.game import Game
from config import get_config

if __name__ == '__main__':
    config = get_config()
    Game(**config).play()
    print('Thanks for playing!')
