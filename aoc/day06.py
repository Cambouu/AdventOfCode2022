import os

def read_file():

    with open(os.path.join('.', 'aoc', 'day06.txt'), 'r') as f:
        signal = f.readline()
        
    return signal


def start_of_packet(signal, msg_size):
    # Initialize packet by size-defined character
    marker = msg_size
    packet = signal[:msg_size]

    # Convert str to set and until every letter is unique
    # the packet will add new characters
    while len(set(packet)) < msg_size:
        if marker < len(signal):
            packet = packet[1:] + signal[marker]
            marker += 1
        else:
            return None
    
    return marker


if __name__ == '__main__':
    signal = read_file()

    marker = start_of_packet(signal, 4)
    print('\nPoint 1')
    print('start-of-packet marker: {0}'.format(marker))

    marker = start_of_packet(signal, 14)
    print('\nPoint 2')
    print('start-of-message marker: {0}'.format(marker))
    