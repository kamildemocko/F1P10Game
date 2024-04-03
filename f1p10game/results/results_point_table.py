race_table = {
    1: 1,
    2: 2,
    3: 4,
    4: 6,
    5: 8,
    6: 10,
    7: 12,
    8: 15,
    9: 18,
    10: 25,
    11: 18,
    12: 15,
    13: 12,
    14: 10,
    15: 8,
    16: 6,
    17: 4,
    18: 2,
    19: 1,
    20: 0,
}

sprint_table = {
    1: 0,
    2: 0,
    3: 1,
    4: 2,
    5: 3,
    6: 4,
    7: 5,
    8: 6,
    9: 7,
    10: 8,
    11: 7,
    12: 6,
    13: 5,
    14: 4,
    15: 3,
    16: 2,
    17: 1,
    18: 0,
    19: 0,
    20: 0,
}


def get_points_for_position(position: int, sprint: bool = False) -> int:
    if position < 1 or position > 20:
        return 0

    if sprint:
        return sprint_table[position]
    else:
        return race_table[position]
