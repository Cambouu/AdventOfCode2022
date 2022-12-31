import os
import json

def read_file():
    # folders will be stored as dict of dict, files as dict of int
    file_system = {}
    # depth will be handled as list to trace during recursion
    folder_depth = []

    with open(os.path.join('.', 'aoc', 'day07.txt'), 'r') as f:
        
        while cmd_line := f.readline().strip():
            # Ignore ..
            if cmd_line == '$ cd ..':
                folder_depth.pop()
            # change in directory is handled as added depth
            elif cmd_line.startswith('$ cd'):
                dir_name = cmd_line[5:]
                folder_depth.append(dir_name)
                file_system = deep_assign(file_system, folder_depth, {})
            # listing of dir is ignored and only files are taken into account
            elif cmd_line[0].isdigit():
                weight, file_name = cmd_line.split(' ')
                folder_depth.append(file_name)
                file_system = deep_assign(file_system, folder_depth, int(weight))
                folder_depth.pop()

    return file_system


def deep_assign(file_system, folder_depth, value):
    # Method to iterate over dicto of dict
    base_folder = folder_depth[0]

    if len(folder_depth) > 1:
        file_system[base_folder] = \
            deep_assign(file_system[base_folder], folder_depth[1:], value)
    
    elif len(folder_depth) == 1:
        file_system[base_folder] = value
    
    return file_system


def dir_weight(file_system, dir_weights={}, folder_depth=[]):
    for key, value in file_system.items():
        # Values are assigned at all depths
        if isinstance(value, int):
            for i in range(len(folder_depth)):
                full_path = os.path.join(*folder_depth[:i+1])
                dir_weights[full_path] = dir_weights.get(full_path, 0) + value
        # Add depth
        elif isinstance(value, dict):
            folder_depth.append(key)
            dir_weights = dir_weight(file_system[key], dir_weights, folder_depth)
            folder_depth.pop()
    
    return dir_weights


if __name__ == '__main__':
    file_system = read_file()
    dir_weights = dir_weight(file_system)

    # json_file_system = json.dumps(file_system, indent = 4)
    # with open(os.path.join('.', 'aoc', 'day07.json'), 'w') as f:
    #     f.write(json_file_system)
    # print(dir_weight(file_system))
    
    print('\nPoint 1')
    print('Sum of directory size: {0}'.format(
        sum(w for w in dir_weights.values() if w <= 100000)
    ))

    print('\nPoint 2')
    required_space = 70000000 - 30000000
    total_space = dir_weights['/']
    free_up = total_space - required_space
    print('Min-sized directory to delete: {0}'.format(
        min(w for w in dir_weights.values() if w >= free_up)
    ))