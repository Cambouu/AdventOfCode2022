import os
import re


def read_file():
    movements_regex = re.compile(r'([U|D|R|L|]) ([0-9]+)')

    with open(os.path.join('.', 'aoc', 'day09.txt'), 'r') as f:
        movements = re.findall(movements_regex, f.read())

    return movements


class Rope:

    def __init__(self) -> None:
        self.nknots = 10 # For point 1: 2, point 2: 10

        # Being (x, y), knot[0] is head and knot[-1] is tail
        self.knots = [[0, 0] for _ in range(self.nknots)]
    
    def __repr__(self) -> str:
        return self.knots.__repr__()
    
    def move_head(self, direction):
        # Move head: knot[0]
        if direction == 'U':
            self.knots[0][1] += 1
        elif direction == 'D':
            self.knots[0][1] -= 1
        elif direction == 'R':
            self.knots[0][0] += 1
        elif direction == 'L':
            self.knots[0][0] -= 1

        # Move all subsequent knots in order, overwriting for the next iteration usage
        for i in range(1, self.nknots):
            self.knots[i] = self.move_tail(self.knots[i - 1], self.knots[i])

    def move_tail(self, knot_head, knot_tail):
        x_distance = knot_head[0] - knot_tail[0]
        y_distance = knot_head[1] - knot_tail[1]

        # Diagram to understand rules is in phone notepad!
        # Basically is illegal to have a distance greater than 2,
        # so the movements are padded until +/-1
        if abs(x_distance) > 1:
            knot_tail[0] += x_distance // abs(x_distance)
            if y_distance != 0:
                knot_tail[1] += y_distance // abs(y_distance)
                
        elif abs(y_distance) > 1:
            knot_tail[1] += y_distance // abs(y_distance)
            if x_distance != 0:
                knot_tail[0] += x_distance // abs(x_distance)
        
        return knot_tail


def positions_visited(movements):
    rope = Rope()
    visited = set()
    visited.add(tuple(rope.knots[-1]))

    for direction, times in movements:
        for _ in range(int(times)):
            rope.move_head(direction)
            visited.add(tuple(rope.knots[-1]))
        # print('{0}-{1}:{2}'.format(direction, times, rope))
    
    return len(visited)


if __name__ == '__main__':
    movements = read_file()

    print('\nTotal of positions visited: {0}'.format(positions_visited(movements)))