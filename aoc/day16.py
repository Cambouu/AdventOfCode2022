import os
import re
test = False


def read_file() -> dict[tuple[int, int]: tuple[int, int]]:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    pipes_regex = re.compile(r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)')

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        pipes = re.findall(pipes_regex, f.read())

    return pipes


if __name__ == '__main__':
    pipes = read_file()

    print('\nPoint 1')

    print('\nPoint 2')