import os

def main():
    '''
    The calories of each Elf are separated by black in txt file
    The idea is to sum all calories to the last value and when a blank line comes up,
    we append a 0
    '''

    calories = [0]
    with open(os.path.join('.','aoc','day01.txt'), 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if len(line) == 0:
            calories.append(0)
        else:
            calories[-1] += int(line)
    
    return calories


if __name__ == '__main__':
    calories = main()

    print('Part 1')
    max_calories = max(calories)
    print('Most caleries: {0}'.format(max_calories))

    print('\nPart 2')
    calories.sort(reverse=True)
    top3_calories = sum(calories[:3])
    print('Top three calories summed: {0}'.format(top3_calories))