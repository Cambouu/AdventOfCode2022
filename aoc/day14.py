import os
import re


def read_file(test=False) -> set[tuple[int, int]]:
    """
    Rocks and dust particles positions will be handled as a set of (x, y) coordinates
    """
    file_ext = '_test' if test else ''
    rocks_regex = r'(\d+),(\d+)'
    rocks = set()

    with open(os.path.join('.', 'aoc', 'day14{0}.txt'.format(file_ext)), 'r') as f:
        line = f.readline().strip()

        while line:
            rocks_found = re.findall(rocks_regex, line)
            rocks_to_add = interconnect_rocks(rocks_found)
            rocks |= rocks_to_add
            line = f.readline().strip()

    return rocks


def interconnect_rocks(rocks_found: tuple[tuple[str, str]]) -> set[tuple[int, int]]:
    """
    Given start and end rocks of a horizontal/vertical line
    Create all points in-between
    """
    rocks = set()

    for i in range(len(rocks_found) - 1):
        pos_current_rock = (int(rocks_found[i][0]), int(rocks_found[i][1]))
        pos_next_rock = (int(rocks_found[i + 1][0]), int(rocks_found[i + 1][1]))

        # Horizontal line of rocks
        if pos_current_rock[0] == pos_next_rock[0]:
            min_y = min(pos_current_rock[1], pos_next_rock[1])
            max_y = max(pos_current_rock[1], pos_next_rock[1])

            for r in range(min_y, max_y + 1):
                rocks.add((pos_current_rock[0], r))

        # Vertical line of rocks
        elif pos_current_rock[1] == pos_next_rock[1]:
            min_x = min(pos_current_rock[0], pos_next_rock[0])
            max_x = max(pos_current_rock[0], pos_next_rock[0])

            for r in range(min_x, max_x + 1):
                rocks.add((r, pos_current_rock[1]))
        
        else: raise
    
    return rocks


def regolith(rocks: set[tuple[int, int]], part=1) -> set[tuple[int, int]]:

    if part == 1:
        lowest_level = max(rocks, key=lambda x: x[1])[1]
    elif part == 2:
        lowest_level = max(rocks, key=lambda x: x[1])[1] + 2
    
    start_dust = (500, 0)
    dust = set()
    prev_dust_state = {start_dust}
    prev_particle_state = [0, 0]

    # Iterate until no dust particle is added
    while dust != prev_dust_state:
        prev_dust_state = dust.copy()
        particle = list(start_dust)
        obstacles = rocks | dust

        # Keep dropping particle until it stalls
        while particle != prev_particle_state:
            prev_particle_state = particle.copy()

            # Vertical drop
            if (particle[0], particle[1] + 1) not in obstacles:
                particle[1] += 1
            # Sway left drop
            elif (particle[0] - 1, particle[1] + 1) not in obstacles:
                particle[0] -= 1
                particle[1] += 1
            # Sway right drop
            elif (particle[0] + 1, particle[1] + 1) not in obstacles:
                particle[0] += 1
                particle[1] += 1
            
            # If dropped lower than lowest level obstacles (Inf) stop dropping and
            # avoid adding the particle to dust
            if part == 1 and particle[1] > lowest_level:
                particle = None
                break
            # If dropped at before lowest level, stall the particle
            elif part == 2 and particle[1] == lowest_level - 1:
                break
        
        if particle:
            dust.add(tuple(particle))
    
    return dust


if __name__ == '__main__':
    rocks = read_file()
    dust = regolith(rocks, 1)

    print('\nPoint 1')
    print('Particles of sand at rest: {0}'.format(len(dust)))

    dust = regolith(rocks, 2)
    print('\nPoint 2')
    print('Particles of sand at rest: {0}'.format(len(dust)))