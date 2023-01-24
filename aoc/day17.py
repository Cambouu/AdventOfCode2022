import os


def read_file() -> str:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        line = f.readline().strip()
        shifts = ''

        while line:
            shifts += line
            line = f.readline().strip()

    return shifts


class Simulation():

    def __init__(self) -> None:
        self.horizontal_size = 7
        self.border_left = 0
        self.border_right = self.horizontal_size + 1
        self.border_bottom = 0
        self.border_top = 0
        self.rocks = set()
        self.number_of_rocks = 0
    
    def add_rocks(self, rocks: set[tuple[int, int]]) -> None:
        self.number_of_rocks += 1
        self.rocks |= rocks

        new_top = max(rocks, key=lambda x: x[1])
        self.border_top = max(self.border_top, new_top[1])

        self.update_bottom(rocks)
    
    def update_bottom(self, rocks: set[tuple[int, int]]) -> None:
        min_j = min(rocks, key=lambda x: x[1])[1]
        max_j = max(rocks, key=lambda x: x[1])[1]

        for j in range(max_j, min_j, -1):
            baseline = {(i, j) for i in range(0, self.border_right)}
            intersect = baseline & self.rocks

            if len(intersect) == self.horizontal_size:
                self.border_bottom = j
                self.rocks = {r for r in self.rocks if r[1] > j}
                return


class Rock():

    def __init__(self, shape: str, sim: Simulation) -> None:
        if shape == '-':
            self.units = {(i, sim.border_top + 4) for i in range(3, 7)}
        elif shape == '+':
            self.units = {
                (4, sim.border_top + 4), 
                (3, sim.border_top + 5), 
                (4, sim.border_top + 5), 
                (5, sim.border_top + 5), 
                (4, sim.border_top + 6)
            }
        elif shape == 'L':
            self.units = {
                (3, sim.border_top + 4), 
                (4, sim.border_top + 4), 
                (5, sim.border_top + 4), 
                (5, sim.border_top + 5), 
                (5, sim.border_top + 6)
            }
        elif shape == '|':
            self.units = {(3, sim.border_top + i) for i in range(4, 8)}
        elif shape == '°':
            self.units = {
                (3, sim.border_top + 4), 
                (4, sim.border_top + 4), 
                (3, sim.border_top + 5), 
                (4, sim.border_top + 5)
            }

    def lower(self, sim: Simulation) -> bool:
        new_units = set()

        for unit in self.units:
            new_unit = (unit[0], unit[1] - 1)
            if (new_unit[1] <= sim.border_bottom) or (new_unit in sim.rocks):
                return False
            new_units.add(new_unit)

        self.units = new_units.copy()
        return True
    
    def push(self, shift: str, sim: Simulation) -> None:
        new_units = set()

        for unit in self.units:
            if shift == '<':
                new_unit = (unit[0] - 1, unit[1])
            elif shift == '>':
                new_unit = (unit[0] + 1, unit[1])
            
            if (new_unit[0] <= sim.border_left) or (new_unit[0] >= sim.border_right) or (new_unit in sim.rocks):
                return
            
            new_units.add(new_unit)
        
        self.units = new_units.copy()


def simulate_part(shifts: str, part: int) -> int:
    if part == 1:
        number_rocks = 2022
    elif part == 2:
        number_rocks = 1000000000000

    sim = Simulation()
    shapes = ['-', '+', 'L', '|', '°']
    shape_counter = -1
    shift_counter = -1

    while sim.number_of_rocks < number_rocks:
        shape_counter = (shape_counter + 1) % len(shapes)
        rock = Rock(shapes[shape_counter], sim)
        rock_moving = True

        while rock_moving:
            shift_counter = (shift_counter + 1) % len(shifts)
            rock.push(shifts[shift_counter], sim)
            rock_moving = rock.lower(sim)
        
        sim.add_rocks(rock.units)
        if sim.number_of_rocks % 1000000 == 0: print(sim.number_of_rocks//1000000)
    
    return sim.border_top


if __name__ == '__main__':
    test = True
    shifts = read_file()

    print('\nPoint 1')
    tall = simulate_part(shifts, 1)
    print('Units tall: {0}'.format(tall))

    print('\nPoint 2')
    tall = simulate_part(shifts, 2)
    print('Units tall: {0}'.format(tall))