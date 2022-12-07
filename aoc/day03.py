import os

def read_file():
    rucksacke = []

    with open(os.path.join('.', 'aoc', 'day03.txt'), 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            half_length = len(line) // 2

            rucksacke.append((set(line[:half_length]), set(line[half_length:])))
    
    return rucksacke

def get_shared_items(rucksacke):
    shared_items = []

    for rucksack1, rucksack2 in rucksacke:
        shared_item = rucksack1 & rucksack2
        assert len(shared_item) == 1
        shared_items.append(shared_item.pop())
    
    return shared_items

def get_badges(rucksacke):
    badges = []

    for i in range(0, len(rucksacke), 3):
        badge = (rucksacke[i][0] | rucksacke[i][1]) & \
            (rucksacke[i+1][0] | rucksacke[i+1][1]) & \
            (rucksacke[i+2][0] | rucksacke[i+2][1])
        assert len(badge) == 1
        badges.append(badge.pop())
    
    return badges

def get_priority(shared_item):
    ascii_code = ord(shared_item)
    if ascii_code <= 90: #A-Z
        return ascii_code - 38
    elif ascii_code >= 91: #a-z
        return ascii_code - 96

def sum_shared_priorities(shared_items):
    sum_priorities = 0

    for shared_item in shared_items:
        sum_priorities += get_priority(shared_item)
    
    return sum_priorities

if __name__ == '__main__':
    rucksacke = read_file()
    
    print('Part 1')
    shared_items = get_shared_items(rucksacke)
    sum_priorities = sum_shared_priorities(shared_items)
    print('Sum of priorities of shared items: {0}'.format(sum_priorities))

    print('\nPart 2')
    badges = get_badges(rucksacke)
    sum_badges = sum_shared_priorities(badges)
    print('Sum of shared badges: {0}'.format(sum_badges))