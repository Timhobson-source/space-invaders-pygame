import math


def clip_value(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def get_lead_enemy(direction, enemies):
    if direction > 0:
        max_x = max([e.x for e in enemies])
        return [e for e in enemies if e.x == max_x][0]
    elif direction < 0:
        min_x = min([e.x for e in enemies])
        return [e for e in enemies if e.x == min_x][0]


def detect_collision(obj1, obj2):
    dist = math.sqrt(
        (obj1.x - obj2.x)**2 +
        (obj1.y - obj2.y)**2
    )
    if dist <= obj1.radius + obj2.radius:
        return True
    return False
