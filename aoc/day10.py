import os


def read_file():

    with open(os.path.join('.', 'aoc', 'day10.txt'), 'r') as f:
        program = f.readlines()

    return program


def cycle_signal(program):
    """
    The computation of addx will be done on the same cycle
    Meaning that if further tasks require a "during" or "before" activity
    it will be taken as the previous cycle
    """
    cycle_execution = []
    x = 1

    for line in program:
        # Independently from action, always add value as either addx or noop
        # have to skip in the first cycle
        cycle_execution.append(x)

        if line.startswith('addx'):
            x += int(line[5:])
            cycle_execution.append(x)
    
    return cycle_execution


def signal_strength(cycle_execution):
    cycles = [20, 60, 100, 140, 180, 220]
    strength = 0

    for cycle in cycles:
        # Draw the value from the previous cycle, because each cycle has the value AFTER
        # Also, the cycles start from 1, so substract 2 in total
        strength += cycle * cycle_execution[cycle - 2]
    
    return strength


def crt_plot(cycle_execution):
    crt_size = 40
    crt_lines = 6

    crt = ['' for _ in range(crt_lines)]
    # First position will always be lit
    crt[0] += '#'

    # Mismatch between cycle and positions, so instead we start cycles on 1 to match
    # As plotting occurs before assignment, the last state is never reached
    for cycle, x in enumerate(cycle_execution[:-1], 1):
        line = cycle // crt_size
        pos = cycle % crt_size

        if x - 1 <= pos <= x + 1:
            crt[line] += ('#')
        else:
            crt[line] += ('.')
    
    return crt


if __name__ == '__main__':
    program = read_file()
    cycle_execution = cycle_signal(program)
    strength = signal_strength(cycle_execution)

    print('\nPoint 1')
    print('Signal strength: {0}'.format(strength))

    print('\nPoint 2')
    print('CRT plot')
    print('\n'.join(crt_plot(cycle_execution)))