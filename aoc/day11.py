import os
import re

def read_file():
    """
    Regex will extract at each position:
    0: monkey number
    1: starting items (full string)
    2: operation, either * or +
    3: operator parameter, either 0-9 or "old"
    4: divisor for test
    5: monkey number if test true
    6: monkey number if test false
    """
    monkey_file = []
    monkey_regex = re.compile((
        r'\s{0}Monkey\s(\d+):\n\s\sStarting\sitems:\s([0-9\s,]+)\n'
        r'\s{2}Operation:\snew\s=\sold\s([\+\*])\s([0-9(?:old)]+)\n'
        r'\s{2}Test:\sdivisible\sby\s(\d+)\n'
        r'\s{4}If\strue:\sthrow\sto\smonkey\s(\d+)\n'
        r'\s{4}If\sfalse:\sthrow\sto\smonkey\s(\d+)'
    ))

    with open(os.path.join('.', 'aoc', 'day11.txt'), 'r') as f:
        monkey_file = f.read()
        matches = re.findall(monkey_regex, monkey_file)
    
    return matches


def define_operation(monkey_line):
    """
    convert from text to lambda functions to be assigned to attributes
    """
    if monkey_line[3] == 'old':
        if monkey_line[2] == '*':
            return lambda x: x * x
        elif monkey_line[2] == '+':
            return lambda x: x + x
    
    else:
        x2 = int(monkey_line[3])
        if monkey_line[2] == '*':
            return lambda x: x * x2
        elif monkey_line[2] == '+':
            return lambda x: x + x2


class Monkey():

    def __init__(self, monkey_line) -> None:
        self.number = int(monkey_line[0])
        self.items = [int(i.strip()) for i in monkey_line[1].split(',')]
        self.operation = define_operation(monkey_line)
        self.divisor = int(monkey_line[4])
        self.divisible = lambda x: (x % self.divisor) == 0
        self.throw_to_true = int(monkey_line[5])
        self.throw_to_false = int(monkey_line[6])

        self.inspection = 0
    
    def __lt__(self, other):
        return self.inspection < other.inspection

    def __repr__(self):
        #return 'Monkey {0}: {1}'.format(self.number, ', '.join(str(i) for i in self.items))
        return 'Monkey {0} inspected items {1} times'.format(self.number, self.inspection)

    def throw_items(self) -> list(tuple(int, int)):
        """
        this object takes all items, computes its respective operation
        and yields a tuple with the info to the designated destination monkey number
        and the computed value
        """
        for item in self.items:
            self.inspection += 1

            new_item = self.operation(item)
            # new_item = new_item // 3 # Uncomment for point 1, comment for point 2

            if self.divisible(new_item):
                yield self.throw_to_true, new_item
            else:
                yield self.throw_to_false, new_item
        
        self.items = []

def greatest_common_divisor(monkeys):
    # https://en.wikipedia.org/wiki/Modular_arithmetic
    """
    Given n prime numbers, the gcd will be the multiplication of them all
    this is used to lower the item value.
    i.e. 3 and 5 have 15 as gcd, meaning every 15 the multiples of these prime numbers will loop
    same as 21 = 1(6/15) can be divided by 3, so can 21, as 36 = 2(6/15)
    """
    gcd = 1
    for monkey in monkeys:
        gcd *= monkey.divisor
    return gcd

def keep_away(monkeys):
    max_rounds = 10000 # 20 for point 1, 10000 for point 2
    gcd = greatest_common_divisor(monkeys)

    for round in range(max_rounds):
        for monkey in monkeys:
            for receive, item in monkey.throw_items():
                # Truncate with gcd
                monkeys[receive].items.append(item % gcd)
        
        # print('\nAfter round {0}'.format(round + 1))
        # print(*monkeys, sep='\n')

    return monkeys


def monkey_business(monkeys):
    # Take largest 2 inspections and multiply them
    monkeys = sorted(monkeys.copy(), reverse=True)
    return monkeys[0].inspection * monkeys[1].inspection


if __name__ == '__main__':
    matches = read_file()
    monkeys = [Monkey(m) for m in matches]
    monkeys = keep_away(monkeys)

    print('Monkey business = {0}'.format(monkey_business(monkeys)))