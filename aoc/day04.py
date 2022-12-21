import os
import re


def read_file():
    assignments_regex = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

    with open(os.path.join('.', 'aoc', 'day04.txt'), 'r') as f:
        assignments_file = f.read()
        assignments = re.findall(assignments_regex, assignments_file)
        
    return assignments


def fully_contains(assignments):
    """
    Examples to count
    .2345678.  2-8 pair1
    ..34567..  3-7 pair2

    .....6...  6-6 pair1
    ...456...  4-6 pair2
    """
    amount = 0
    for assignment in assignments:

        pair1 = (int(assignment[0]), int(assignment[1]))
        pair2 = (int(assignment[2]), int(assignment[3]))
        if ((pair1[0] <= pair2[0]) and (pair1[1] >= pair2[1])) or \
            ((pair1[0] >= pair2[0]) and (pair1[1] <= pair2[1])):

            amount += 1
    
    return amount


def overlaps(assignments):
    """
    Examples to count
    ....567..  5-7 pair1
    ......789  7-9 pair2

    .2345678.  2-8 pair1
    ..34567..  3-7 pair2
    """
    overlap = 0
    for assignment in assignments:

        pair1 = (int(assignment[0]), int(assignment[1]))
        pair2 = (int(assignment[2]), int(assignment[3]))
        if ((pair1[0] <= pair2[1]) and (pair1[1] >= pair2[0])):

            overlap += 1
            
    return overlap


if __name__ == '__main__':
    assignments = read_file()

    print('\nPoint 1')
    print(fully_contains(assignments))

    print('\nPoint 2')
    print(overlaps(assignments))