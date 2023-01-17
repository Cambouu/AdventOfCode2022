import os


def read_file1(test=False) -> list[tuple]:
    """
    For the first part the file will be read in triplets:
    first line = left pair
    second line = right pair
    third line = empty line
    Each pair will be stored in a tuple
    """
    file_ext = '_test' if test else ''
    packet = []

    with open(os.path.join('.', 'aoc', 'day13{0}.txt'.format(file_ext)), 'r') as f:
        line = f.readline().strip() # left pair

        while line:
            pair_1 = eval(line)
            line = f.readline().strip() # right pair
            pair_2 = eval(line)
            packet.append((pair_1, pair_2))
            line = f.readline().strip() # empty line
            line = f.readline().strip() # left pair

    return packet


def read_file2(test=False):
    """
    For the second part we don't care about pairs so we read all lines ignoring blanks
    """
    file_ext = '_test' if test else ''
    packet = []

    with open(os.path.join('.', 'aoc', 'day13{0}.txt'.format(file_ext)), 'r') as f:
        
        for line in f.readlines():
            line = line.strip()

            if line:
                packet.append(eval(line))
            

    return packet


def packet_order(pairs):
    """
    First part we evaluate each pair and if these are ordered,
    then we add the index to a list to be summed at the end
    """
    right_order_packets = []

    for i, pair in enumerate(pairs, 1):
        if is_sorted(*pair):
            right_order_packets.append(i)
    
    return sum(right_order_packets)
        

def is_sorted(left, right):
    """
    Recursively determine whether left is smaller than right
    bool if found a difference, if both cases are equal returns None
    """
    if type(left) != type(right):
        if isinstance(left, int):
            return is_sorted([left], right)
        elif isinstance(right, int):
            return is_sorted(left, [right])

    elif isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    elif isinstance(left, list) and isinstance(right, list):
        min_len = min(len(left), len(right))

        for i, j in zip(left[:min_len], right[:min_len]):
            comparison = is_sorted(i, j)

            if isinstance(comparison, bool):
                return comparison

        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False
    
    return None


def bubble_sort_packet(packet):
    """
    From part 1 we have implemented __lt__() for the object comparison
    Now we use that method in our own custom sorting algorithm: bubble sort
    """
    packet += [[[2]], [[6]]]

    for end in range(len(packet) - 1, 0, -1):
        for start in range(end):

            if not is_sorted(packet[start], packet[end]):
                packet[end], packet[start] = packet[start], packet[end]
    
    return packet


if __name__ == '__main__':
    packet = read_file1()

    print('\nPoint 1')
    print('Sum of right order packet indexes: {0}'.format(packet_order(packet)))

    packet = read_file2()
    packet = bubble_sort_packet(packet)
    decoder = (packet.index([[2]]) + 1) * (packet.index([[6]]) + 1)
    print('\nPoint 2')
    print('Divider packets multiplication: {0}'.format(decoder))