

from abc import abstractmethod


def build_formation(screen_handler, nrows=4, ncols=10):
    # NOTE - this is pretty bad/confusing code, needs a refactor
    # potentially even move this somewhere else
    from config import get_config
    config = get_config()
    r = config['enemy']['radius']
    min_x = config['window']['left_horizontal_buffer']
    max_x = screen_handler.screen.get_width(
    ) - config['window']['right_horizontal_buffer']
    vel = config['enemy']['speed']

    min_y = config['window']['top_vertical_buffer']

    extra = 1  # extra space between
    for x in range(min_x + r, min_x + 2*r*(ncols + 1 + extra), 2*r*(1+extra)):
        if x > max_x - r:
            raise ValueError(
                "Too many enemies to fit on one row for given size.")
        for y in range(min_y + r, min_y + 2*r*(nrows + 1 + extra), 2*r*(1 + extra)):
            if y == min_y + r:
                screen_handler.screen_object_factory.create_shooting_enemy(
                    x, y, vel, r)
            else:
                screen_handler.screen_object_factory.create_standard_enemy(
                    x, y, vel, r)


class Formation(ABC):
    """
    Class to represent an enemy formation and handle its movement.

    Formation is a grid of enemies, but could be generalised to include
    other shapes.
    """

    id_counter = 0

    # what info does this object actually need?
    # - the enemies on the screen (that havent been killed)
    # - the right/left most edges of the formation

    # what info should this object return?
    # - how the formation should move (when to turn around, etc...)

    def __init__(self, id: int):
        self._id = self.id_counter
        self.id_counter += 1

    def __contains__(self, obj):
        return obj.id in self.id

    @property
    def id(self):
        return self._id

    def __eq__(self, formation):
        return self.id == formation.id

    @abstractmethod
    def build(self, screen_handler, id):
        pass


class RectangularFormation(Formation):
    def __init__(self, id: int, nrows: int = 4, ncols: int = 10):
        self.nrows = nrows
        self.ncols = ncols
        super().__init__(id)

    def build(self, screen_handler, id):
        pass
