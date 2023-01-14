import os

def read_file():

    with open(os.path.join('.', 'aoc', 'day08.txt'), 'r') as f:
        grid = f.readlines()

    return grid


def count_visible_trees(grid):
    count = 0
    grid_size = len(grid)

    for i in range(grid_size):
        for j in range(grid_size):
            # Always count border trees
            if (i == 0) or (j == 0) or (i == grid_size) or (j == grid_size):
                count += 1
            else:
                count += tree_visibility(grid, i, j)
    
    return count
                

def tree_visibility(grid, i, j):
    base_tree = int(grid[i][j])
    grid_size = len(grid)
    visible_direction = [True, True, True, True] # [North, South, East, West]

    # Only one loop to compare against all horizontal and vertical trees respective to tree[i][j]
    for k in range(grid_size):

        if int(grid[k][j]) >= base_tree:
            # North
            if k < i:
                visible_direction[0] = False
            # South
            elif k > i:
                visible_direction[1] = False
        
        if int(grid[i][k]) >= base_tree:
            # East
            if k < j:
                visible_direction[2] = False
            # West
            elif k > j:
                visible_direction[3] = False
    
    return any(visible_direction)


def highest_scenic_score(grid):
    score = 0
    grid_size = len(grid)

    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            base_tree = int(grid[i][j])
            visibility = [0, 0, 0, 0] # North, South, East, West

            # North
            for k in range(i - 1, -1, -1):
                visibility[0] += 1
                if int(grid[k][j]) >= base_tree: break
            # South
            for k in range(i + 1, grid_size):
                visibility[1] += 1
                if int(grid[k][j]) >= base_tree: break
            # East
            for k in range(j + 1, grid_size):
                visibility[2] += 1
                if int(grid[i][k]) >= base_tree: break
            # West
            for k in range(j - 1, -1, -1):
                visibility[3] += 1
                if int(grid[i][k]) >= base_tree: break
            
            visibility_score = visibility[0] * visibility[1] * visibility[2] * visibility[3]
            score = max(score, visibility_score)
    
    return score


if __name__ == '__main__':
    grid = read_file()
    
    print('\nPoint 1')
    print('Amount of visible trees: {0}'.format(count_visible_trees(grid)))

    print('\nPoint 2')
    print('Highest scenic score: {0}'.format(highest_scenic_score(grid)))