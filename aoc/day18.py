import os
import re
import numpy as np

def read_file() -> set[tuple[int]]:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    coordinates_regex = re.compile(r'(\d+),(\d+),(\d+)')

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        coordinates = re.findall(coordinates_regex, f.read())
        coordinates = {(int(x), int(y), int(z)) for x, y, z in coordinates}

        limits = (
            max(cubes, key=lambda cube: cube[0])[0] - 
            min(cubes, key=lambda cube: cube[0])[0], 
            max(cubes, key=lambda cube: cube[1])[1] - 
            min(cubes, key=lambda cube: cube[1])[1], 
            max(cubes, key=lambda cube: cube[2])[2] - 
            min(cubes, key=lambda cube: cube[2])[2], 
        )
        cubes = np.zeros(limits, dtype=int)

        for x, y, z in coordinates:
            cubes[x, y, z] = 1

    return cubes


def singleton_dim(cubes: set[tuple[int]], x_cut=None, y_cut=None, z_cut=None) -> set[tuple[int]]:
    
    if x_cut is not None:
        return {(y, z) for x, y, z in cubes if x == x_cut}
    elif y_cut is not None:
        return {(x, z) for x, y, z in cubes if y == y_cut}
    elif z_cut is not None:
        return {(x, y) for x, y, z in cubes if z == z_cut}


def watersheds(cubes, x_lim=None, y_lim=None, z_lim=None) -> int:
    contour_count = 0

    if x_lim is not None:
        slice_prev = set()
        for x_cut in range(x_lim[0], x_lim[1] + 1):
            slice_current = singleton_dim(cubes, x_cut=x_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current
        slice_prev = set()
        for x_cut in range(x_lim[1], x_lim[0] - 1, -1):
            slice_current = singleton_dim(cubes, x_cut=x_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current

    elif y_lim is not None:
        slice_prev = set()
        for y_cut in range(y_lim[0], y_lim[1] + 1):
            slice_current = singleton_dim(cubes, y_cut=y_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current
        slice_prev = set()
        for y_cut in range(y_lim[1], y_lim[0] - 1, -1):
            slice_current = singleton_dim(cubes, y_cut=y_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current
    
    elif z_lim is not None:
        slice_prev = set()
        for z_cut in range(z_lim[0], z_lim[1] + 1):
            slice_current = singleton_dim(cubes, z_cut=z_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current
        slice_prev = set()
        for z_cut in range(z_lim[1], z_lim[0] - 1, -1):
            slice_current = singleton_dim(cubes, z_cut=z_cut)
            contour = slice_current - slice_prev
            contour_count += len(contour)
            slice_prev = slice_current
    
    return contour_count


def count_sides(cubes: set[tuple[int]]) -> int:
    contour_count = 0

    x_lim = (
        min(cubes, key=lambda cube: cube[0])[0], 
        max(cubes, key=lambda cube: cube[0])[0]
    )
    contour_count += watersheds(cubes, x_lim=x_lim)

    y_lim = (
        min(cubes, key=lambda cube: cube[1])[1], 
        max(cubes, key=lambda cube: cube[1])[1]
    )
    contour_count += watersheds(cubes, y_lim=y_lim)

    z_lim = (
        min(cubes, key=lambda cube: cube[2])[2], 
        max(cubes, key=lambda cube: cube[2])[2]
    )
    contour_count += watersheds(cubes, z_lim=z_lim)

    return contour_count


if __name__ == '__main__':
    test = False
    cubes = read_file()

    print('\nPoint 1')
    print('Surface area: {0}'.format(count_sides(cubes)))

    print('\nPoint 2')