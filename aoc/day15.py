import os
import re


def read_file(test: bool = False) -> dict[tuple[int, int]: tuple[int, int]]:
    """
    Sensors data structure will be a dictionary, whose keys are sensors and values are beacons
    relationship: sensor *..1 beacons
    """
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
    """
    For part 1, we will iterate over all sensor areas and intersect them with the row of interest
    """
    coverage = set()

    for sensor, beacon in sensors.items():
        coverage |= build_diamond(sensor, beacon, row_of_interest)
    
    return coverage


def build_diamond(sensor: tuple[int, int], beacon: tuple[int, int], row_of_interest: int) -> set[tuple[int, int]]:
    """
    We add all posible (x, y) coordinates that satisfy the manhattan range between the sensor and the beacon
    Only 1 for loop is needed as it can be reflected.
    The loop is constrained by x + y < manhattan, as we are given y, then the formula is cleared as:
    x < manhattan - y
    But we have to know y respect to the center of the diamond, so it becomes:
    x < manhattan - (sensor_y - row_of_interest)
    To address above/below row_of_interest with respect to sensor_y we take the abs()
    """
    diamond = set()
    manhattan = manhattan_distance(sensor, beacon)
    
    for i in range(0, manhattan - abs(sensor[1] - row_of_interest) + 1):

        diamond.add((sensor[0] + i, row_of_interest)) # right side
        diamond.add((sensor[0] - i, row_of_interest)) # left side
            
    if beacon in diamond: diamond.remove(beacon)
    if sensor in diamond: diamond.remove(sensor)

    return diamond


def tuning_frequency(sensors: dict[tuple[int, int]: tuple[int, int]]) -> int:
    """
    As there is only one point not covered by any sensor, it means the point has to be
    surrounded by 4 different beacons and be exactly outside the perimeter of each sensor range.
    What we then do is extend the perimeter by 1 for all sensors and intersect all combinations
    of 4 sensors, yielding all points possible.
    Previous case fails if the point is in a corner or if the beacons are not in juxtaposition.
    To solve this, we just iterate over all posible 4-fold intersections asking whether they
    belong to the range of any sensor
    """
    perimeters = {s: build_perimeter(s, b) for s, b in sensors.items()}
    intersects = set()
    
    sensor_keys = list(perimeters.keys())
    for i1, sensor1 in enumerate(sensor_keys[:-3]):

        for i2, sensor2 in enumerate(sensor_keys[i1 + 1:-2], i1 + 1):
            if not perimeters[sensor1] & \
                perimeters[sensor2]: continue

            for i3, sensor3 in enumerate(sensor_keys[i2 + 1:-1], i2 + 1):
                if not perimeters[sensor1] & \
                    perimeters[sensor2] & \
                    perimeters[sensor3]: continue

                for sensor4 in sensor_keys[i3 + 1:]:
                    intersect = perimeters[sensor1] & \
                        perimeters[sensor2] & \
                        perimeters[sensor3] & \
                        perimeters[sensor4]

                    if intersect:
                        intersects |= intersect.copy()
    
    real_intersect = None
    for intersect in intersects:
        if not within_sensors(sensors, intersect):
            real_intersect = intersect

    return real_intersect
        

def build_perimeter(sensor: tuple[int, int], beacon: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Creates a set of points corresponding to the outer perimeter of a sensor-beacon composition
    There is only one loop because the diamond can be decomposed into 4 quadrants
    each will be the reflex of the other one
    """
    perimeter = set()
    # We don't want the exact perimeter but rather the outer limiting one
    manhattan = manhattan_distance(sensor, beacon) + 1
    border = 4000000

    for i in range(0, manhattan + 1):
        x_plus = sensor[0] + i
        x_neg = sensor[0] - i
        y_plus = sensor[1] + manhattan - i
        y_neg = sensor[1] - manhattan + i

        # quadrant 1
        if 0 <= x_plus <= border and 0 <= y_plus <= border:
            perimeter.add((x_plus, y_plus))
        # quadrant 2
        if 0 <= x_plus <= border and 0 <= y_neg <= border:
            perimeter.add((x_plus, y_neg))
        # quadrant 3
        if 0 <= x_neg <= border and 0 <= y_neg <= border:
            perimeter.add((x_neg, y_neg))
        # quadrant 4
        if 0 <= x_neg <= border and 0 <= y_plus <= border:
            perimeter.add((x_neg, y_plus))

    return perimeter


def within_sensors(sensors: dict[tuple[int, int]: tuple[int, int]], point: tuple[int, int]) -> bool:
    """
    Determines whether a given point falls within the range of any sensor
    """
    for sensor, beacon in sensors.items():
        sensor_range = manhattan_distance(sensor, beacon)
        distance = manhattan_distance(sensor, point)
        if distance <= sensor_range:
            return True
    return False


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

    print('\nPoint 2')
    available_pos = tuning_frequency(sensors)
    print('Tunning frequency: {0}'.format(available_pos[0] * 4000000 + available_pos[1]))