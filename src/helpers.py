

def clip_value(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def generate_enemy_grid(screen_handler, nrows=4, ncols=10):
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
                screen_handler.create_shooting_enemy(x, y, vel, r)
            else:
                screen_handler.create_standard_enemy(x, y, vel, r)


# @lru_cache(maxsize=10)
def get_lead_enemy(direction, enemies):
    if direction > 0:
        max_x = max([e.x for e in enemies])
        return [e for e in enemies if e.x == max_x][0]
    elif direction < 0:
        min_x = min([e.x for e in enemies])
        return [e for e in enemies if e.x == min_x][0]
