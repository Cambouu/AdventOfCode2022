import os
import re
import numpy as np
from scipy import ndimage

def read_file() -> np.ndarray:

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    coordinates_regex = re.compile(r'(\d+),(\d+),(\d+)')

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        coordinates = re.findall(coordinates_regex, f.read())
        coordinates = {(int(x), int(y), int(z)) for x, y, z in coordinates}

        # Parse coordinates to start from zero in 3d binary image
        limits = (
            (min(coordinates, key=lambda coordinate: coordinate[0])[0], 
            max(coordinates, key=lambda coordinate: coordinate[0])[0]),  

            (min(coordinates, key=lambda coordinate: coordinate[1])[1], 
            max(coordinates, key=lambda coordinate: coordinate[1])[1]),  

            (min(coordinates, key=lambda coordinate: coordinate[2])[2], 
            max(coordinates, key=lambda coordinate: coordinate[2])[2])
        )
        cubes = np.zeros(tuple(l[1] - l[0] + 1 for l in limits), dtype=bool)
        
        # Create a 3d binary image and assign coordinates as True
        for x, y, z in coordinates:
            cubes[x - limits[0][0], y - limits[1][0], z - limits[2][0]] = True

    return cubes


def watersheds(cubes: np.ndarray, part=1) -> int:
    """
    The idea of watersheds is to submerge the figure layer by layer,
    after each iteration the new positions will be considered the contour at that point.
    But in this case we just need to count the contour pixels.
    """
    contour_count = 0
    if part == 2:
        cubes = ndimage.binary_fill_holes(cubes)
    
    for dimension in range(3):

        # Submersion will yield a singleton dimension, parsing the 3d image to 2d
        shape = list(cubes.shape)
        shape.pop(dimension)

        # We want both faces front and back on the same dimension
        slice_front_prev = np.zeros(shape, dtype=bool)
        slice_back_prev = np.zeros(shape, dtype=bool)

        for cut in range(cubes.shape[dimension]):
            slice_front_current = np.take(cubes, cut, dimension)
            slice_back_current = np.take(cubes, cubes.shape[dimension] - 1 - cut, dimension)

            # We compare the slide vs the previous one to obtain only contours
            contour_front = slice_front_current & ~slice_front_prev
            contour_back = slice_back_current & ~slice_back_prev

            slice_front_prev = slice_front_current.copy()
            slice_back_prev = slice_back_current.copy()

            contour_count += contour_front.sum() + contour_back.sum()
    
    return contour_count


if __name__ == '__main__':
    test = False
    cubes = read_file()

    print('\nPoint 1')
    print('Surface area: {0}'.format(watersheds(cubes, 1)))

    print('\nPoint 2')
    print('Surface area: {0}'.format(watersheds(cubes, 2)))