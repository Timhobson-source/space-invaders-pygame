

def build_formation_grid(radius, left_buffer, top_buffer, nrows, ncols,
                         **kwargs):
    r = radius
    min_x = left_buffer
    min_y = top_buffer

    extra = 1  # extra space between

    # Probably should clean up the grid definition below. Try to make it
    # obvious thats what the grid should be for the reader.
    grid = []
    for x in range(min_x + r, min_x + 2*r*(ncols + 1 + extra), 2*r*(1 + extra)):
        for y in range(min_y + r, min_y + 2*r*(nrows + 1 + extra), 2*r*(1 + extra)):
            grid.append((x, y))
    return grid


def calc_move_counter_level(grid, radius, velocity, right_buffer, width, **kwargs):
    max_allowed_x_on_screen = width - right_buffer
    max_point_in_grid = max(x for x, y in grid) + radius
    return (max_allowed_x_on_screen - max_point_in_grid) // velocity


def build_enemy_formation(screen_handler, nrows=4, ncols=10):
    from config import get_config
    config = get_config()

    vel = config['enemy']['speed']
    r = config['enemy']['radius']
    grid = build_formation_grid(nrows=nrows, ncols=ncols, **config['window'], **config['enemy'])
    move_counter_level = calc_move_counter_level(
        grid=grid, velocity=vel, **config['enemy'], **config['window'])

    first_layer_y = min([y for x, y in grid])
    for x, y in grid:
        if y == first_layer_y:
            enemy = screen_handler.screen_object_factory.create_shooting_enemy(x, y, vel, r)
            enemy.set_move_counter_max_level(move_counter_level)
        else:
            enemy = screen_handler.screen_object_factory.create_standard_enemy(x, y, vel, r)
            enemy.set_move_counter_max_level(move_counter_level)
