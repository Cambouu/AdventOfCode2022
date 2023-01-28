import os
import re

def read_file() -> dict:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    jobs_regex = re.compile(r'(\w{4}): (.+)')

    jobs = {}
    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        found = re.findall(jobs_regex, f.read())

        for monkey, job in found:
            if job.isnumeric():
                jobs[monkey] = int(job)
            else:
                # Result is [operand_1, operation, operand_2]
                jobs[monkey] = job.split(' ')

    return jobs


def dfs(jobs: dict, monkey: str = 'root') -> int:
    """
    Depth first search implementation based on recursiveness
    """
    if isinstance(jobs[monkey], int):
        return jobs[monkey]
    
    else:
        monkey_1 = jobs[monkey][0]
        operation = jobs[monkey][1]
        monkey_2 = jobs[monkey][2]

        if operation == '+':
            return dfs(jobs, monkey_1) + dfs(jobs, monkey_2)

        elif operation == '-':
            return dfs(jobs, monkey_1) - dfs(jobs, monkey_2)

        elif operation == '*':
            return dfs(jobs, monkey_1) * dfs(jobs, monkey_2)

        elif operation == '/':
            return dfs(jobs, monkey_1) // dfs(jobs, monkey_2)


def midpoint_approximation(jobs: dict) -> tuple[int]:
    """
    Idea based on: https://github.com/tbpaolini/Advent-of-Code/blob/master/2022/Day%2021/day_21.py
    This uses gradient decent but I prefer midpoint because it's easier to implement.
    The idea of comparison is to change the operation of root to substraction and get zero as result.
    First some random range of numbers were assigned to humn until both results contained different signs.
    Then midpoint was implemented, where it was updated according to boundary signs to get closer to zero.
    Implementation of midpoint is without floating point there is a error margin when the method returns.
    """
    jobs['root'][1] = '-'
    # Cherry-picked range size
    range_size = 64
    lbound = -2**range_size
    ubound = 2**range_size
    midpoint = (lbound + ubound) // 2

    while True:

        jobs['humn'] = midpoint
        mdiff = dfs(jobs)

        jobs['humn'] = ubound
        udiff = dfs(jobs)

        # Return the point where zero occurs and its error margin
        if mdiff == 0:
            return midpoint, abs(ubound - midpoint)
        elif udiff == 0:
            return ubound, abs(ubound - midpoint)
        else:
            msign = mdiff // abs(mdiff)
            usign = udiff // abs(udiff)

        # If upper bound and midpoint have the same sign, it means that the zero
        # occurs between midpoint and lower bound, and viceversa
        if usign == msign:
            ubound = midpoint
        else:
            lbound = midpoint
        
        midpoint = (lbound + ubound) // 2


if __name__ == '__main__':
    test = False
    jobs = read_file()

    print('\nPoint 1')
    print('Monkey root yells: {0}'.format(dfs(jobs)))

    print('\nPoint 2')
    midpoint, error_margin = midpoint_approximation(jobs)
    print('Human should yell: {0} +/-{1}'.format(midpoint, error_margin))