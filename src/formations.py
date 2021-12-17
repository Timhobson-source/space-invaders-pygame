

def build_formation(screen_handler, nrows=4, ncols=10):
    # NOTE - this is pretty bad/confusing code, needs a refactor
    # potentially even move this somewhere else
    from config import get_config
    config = get_config()

    r = config['enemy']['radius']
    min_x = config['window']['left_buffer']
    max_x = screen_handler.screen.get_width() - config['window']['right_buffer']
    vel = config['enemy']['speed']

    min_y = config['window']['top_buffer']

    extra = 1  # extra space between
    for x in range(min_x + r, min_x + 2*r*(ncols + 1 + extra), 2*r*(1+extra)):
        if x > max_x - r:
            raise ValueError(
                "Too many enemies to fit on one row for given size.")
        for y in range(min_y + r, min_y + 2*r*(nrows + 1 + extra), 2*r*(1 + extra)):
            if y == min_y + r:
                screen_handler.screen_object_factory.create_shooting_enemy(x, y, vel, r)
            else:
                screen_handler.screen_object_factory.create_standard_enemy(x, y, vel, r)
