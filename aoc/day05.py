import os
import re
from copy import deepcopy

def read_file():
    movements_regex = re.compile(r'move (\d+) from (\d+) to (\d+)')

    with open(os.path.join('.', 'aoc', 'day05.txt'), 'r') as f:
        line = f.readline()
        arrangements = []

        # Read until first empty line to get stacks structure
        while len(line.strip()) != 0:
            arrangements.append(line)
            line = f.readline()
        stacks = generate_stacks(arrangements)

        # Read the rest as movements (quantity, from_stack, to_stack)
        assignments_file = f.read()
        movements = re.findall(movements_regex, assignments_file)
        movements = [(int(i[0]), int(i[1]), int(i[2])) for i in movements]
        
    return stacks, movements


def generate_stacks(arrangements):

    # Last line corresponds to indexes of stack
    stacks_indexes = arrangements.pop()
    stacks_indexes = stacks_indexes.strip().split()
    stacks_indexes = [int(i) for i in stacks_indexes]
    stack_len = len(stacks_indexes)

    # Stacks are always on the same position in the str
    # and can be mapped with a sequential formula
    stacks = dict(zip(stacks_indexes, [[] for _ in range(stack_len)]))
    sequence = lambda x: x * 4 + 1

    # Build stacks from bottom to top, top-most item is last in list
    for arrangement in arrangements[::-1]:
        for stack_pos in range(stack_len):
            crate = arrangement[sequence(stack_pos)]

            if crate != ' ':
                stacks[stack_pos + 1].append(crate)
    
    return stacks


def move_crates(stacks, movements, point):
    stacks = deepcopy(stacks)

    for quantity, from_stack, to_stack in movements:
        if point == 1:
            for _ in range(quantity):
                stacks[to_stack].append(stacks[from_stack].pop())

        elif point == 2:
            stacks[to_stack] += stacks[from_stack][-quantity:]
            stacks[from_stack] = stacks[from_stack][:-quantity]
    
    return stacks


def get_message(stacks):
    msg = ''

    for stack in stacks.values():
        msg += stack[-1]
    
    return msg


if __name__ == '__main__':
    stacks, movements = read_file()

    stacks1 = move_crates(stacks, movements, 1)
    msg1 = get_message(stacks1)
    print('\nPoint 1')
    print(msg1)

    stacks2 = move_crates(stacks, movements, 2)
    msg2 = get_message(stacks2)
    print('\nPoint 2')
    print(msg2)
    