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
                jobs[monkey] = job.split(' ')

    return jobs


def dfs(jobs: dict, monkey: str = 'root') -> int:
    
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


if __name__ == '__main__':
    test = False
    jobs = read_file()

    print('\nPoint 1')
    print('Monkey root yells: {0}'.format(dfs(jobs)))

    print('\nPoint 2')