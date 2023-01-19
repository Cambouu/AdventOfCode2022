import os
import re


def read_file(test: bool = False) -> dict[tuple[int, int]: tuple[int, int]]:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    sensor_regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        sensors_found = re.findall(sensor_regex, f.read())
        sensors = {(int(s[0]), int(s[1])): (int(s[2]), int(s[3])) for s in sensors_found}

    return sensors


def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def sensor_coverage(sensors: dict[tuple[int, int]: tuple[int, int]], row_of_interest: int) -> set[tuple[int, int]]:
    coverage = set()

    for sensor, beacon in sensors.items():
        coverage |= build_diamond(sensor, beacon, row_of_interest)
    
    return coverage


def build_diamond(sensor: tuple[int, int], beacon: tuple[int, int], row_of_interest: int) -> set[tuple[int, int]]:
    diamond = set()
    manhattan = manhattan_distance(sensor, beacon)
    
    for i in range(0, manhattan - abs(sensor[1] - row_of_interest) + 1):

        diamond.add((sensor[0] + i, row_of_interest)) # right
        diamond.add((sensor[0] - i, row_of_interest)) # left
            
    if beacon in diamond: diamond.remove(beacon)
    if sensor in diamond: diamond.remove(sensor)

    return diamond


def tuning_frequency(sensors: dict[tuple[int, int]: tuple[int, int]]) -> int:
    manhattans = {sensor: manhattan_distance(sensor, beacon) for sensor, beacon in sensors.items()}
    multiplier = 4000000
    
    for i in range(multiplier):
        for j in range(multiplier):
            if j%10000==0: print(i, j)

            within_sensor = False
            for sensor, manhattan in manhattans.items():
                if manhattan_distance(sensor, (i, j)) <= manhattan:
                    within_sensor = True
            if not within_sensor:
                return i * multiplier + j
            

if __name__ == '__main__':
    test = False
    if test:
        row_of_interest = 10
    else:
        row_of_interest = 2000000

    sensors = read_file(test)
    coverage = sensor_coverage(sensors, row_of_interest)

    print('\nPoint 1')
    print('Unavailable positions: {0}'.format(len(coverage)))

    # print('\nPoint 2')
    # print('Tunning frequency: {0}'.format(tuning_frequency(sensors)))