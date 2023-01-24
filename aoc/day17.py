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
    """
    Object containing the list of levels of fallen rocks
    """
    def __init__(self) -> None:
        # Basic layout containing the boundaries
        self.layout = [int('100000001', 2)]
        # Base layour containing a filled level
        self.bottom_layout = [int('111111111', 2)]
        self.rocks = self.bottom_layout + self.layout * 4

        # Reference to the highest rock
        self.real_top = 0
        # Reference of the relative floor
        self.virtual_bottom = 0
        # Reference the full relative stack size
        self.virtual_top = len(self.rocks)
        self.number_of_rocks = 0
    
    def print(self) -> None:
        for r in self.rocks[::-1]:
            print(bin(r))
    
    def add_rock(self, rocks: list[int], rock_virtual_height: int) -> None:
        """
        Rocks are added with or-gate to the full tower.
        The incoming rocks have already been validated and it's not important to
        track them anymore individually
        """
        self.number_of_rocks += 1
        for i in range(len(rocks)):
            self.rocks[rock_virtual_height + i] |= rocks[i]

        # It should always have a 4 overhead free layout
        # In case the added rock modifies the top level, 
        # we add base layouts accordingly to fulfill the 4 layer need
        self.rocks += self.layout * max(0, rock_virtual_height + i - self.real_top)
        self.real_top = max(self.real_top, rock_virtual_height + i)
        self.virtual_top = len(self.rocks)

        self.update_bottom((rock_virtual_height, min(rock_virtual_height + len(rocks), self.virtual_top)))
    
    def update_bottom(self, height_range: tuple[int, int]) -> None:
        """
        In case a line gets full, there is no need to track what is below it anymore
        Here we delete the list below the full level and record the reference value
        to have the real full value at the end and not only the relative.
        Also we dont evaluate the entire column, just the range where the new rock was inserted
        """
        for h in range(height_range[0], height_range[1]):

            if self.rocks[h] == self.bottom_layout[0]:
                self.rocks = self.rocks[h:]
                self.real_top -= h
                self.virtual_bottom += h
                self.virtual_top = len(self.rocks)
                return


class Rock():
    """
    Rocks will be handled as list of binaries
    """
    def __init__(self, shape: str, sim: Simulation) -> None:
        if shape == '-'  : self.units = [int('00111100', 2)]
        elif shape == '+': self.units = [int('00010000', 2), int('00111000', 2), int('00010000', 2)]
        elif shape == 'L': self.units = [int('00111000', 2), int('00001000', 2), int('00001000', 2)]
        elif shape == '|': self.units = [int('00100000', 2)] * 4
        elif shape == '°': self.units = [int('00110000', 2)] * 2

        self.virtual_height = sim.virtual_top - 1
        self.rock_len = len(self.units)

    def print(self) -> None:
        layout = int('100000001', 2)
        for r in self.units[::-1]:
            print(bin(r | layout))

    def lower(self, sim: Simulation) -> bool:
        """
        Determine whether there is collision in a lower level,
        then reduce the level of insertion to the rock
        """
        for i, h in enumerate(range(self.virtual_height, min(self.virtual_height + self.rock_len, sim.virtual_top))):
            if (h - 1 <= 0) or (self.units[i] & sim.rocks[h - 1]):
                return False
        
        self.virtual_height -= 1

        return True
    
    def push(self, shift: str, sim: Simulation) -> None:
        """
        Test for collisions when moving sideways
        Then perform bitwise shift operation
        """
        if shift == '<':
            new_units = [unit << 1 for unit in self.units]
        elif shift == '>':
            new_units = [unit >> 1 for unit in self.units]

        for i, h in enumerate(range(self.virtual_height, min(self.virtual_height + self.rock_len, sim.virtual_top))):    
            if new_units[i] & sim.rocks[h]:
                return
        
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
        # Cycling is handled as modulo of the full length
        shape_counter = (shape_counter + 1) % len(shapes)
        rock = Rock(shapes[shape_counter], sim)
        rock_moving = True

        # After moving the rock, if it's not possible
        # will exit the loop with the last position of the rock
        while rock_moving:
            shift_counter = (shift_counter + 1) % len(shifts)
            rock.push(shifts[shift_counter], sim)
            rock_moving = rock.lower(sim)
        
        # Add rock the cannot be moved anymore
        sim.add_rock(rock.units, rock.virtual_height)
        # if sim.number_of_rocks % 1000000 == 0: print(sim.number_of_rocks//1000000)
    
    # We deal also with relativity of height, 
    # so we have to take into account the relative top plus the full base height
    return sim.real_top + sim.virtual_bottom


if __name__ == '__main__':
    test = True
    shifts = read_file()

    print('\nPoint 1')
    tall = simulate_part(shifts, 1)
    print('Units tall: {0}'.format(tall))

    print('\nPoint 2')
    # tall = simulate_part(shifts, 2)
    # print('Units tall: {0}'.format(tall))