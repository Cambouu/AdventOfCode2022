import os
import math


def read_file() -> list[str]:

    with open(os.path.join('.', 'aoc', 'day12.txt'), 'r') as f:
        heightmap = f.readlines()
        heightmap = [line.strip() for line in heightmap]

    return heightmap


def get_pos(
    heightmap: list[str]) -> tuple[list[str], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """
    Returns the position of start and end
    Also replaces the start and end letters for lowest and highes places
    """

    start_char = 'S'
    end_char = 'E'

    for i, line in enumerate(heightmap):
        start_char_found: int = line.find(start_char)
        end_char_found: int = line.find(end_char)

        if start_char_found != -1:
            start_pos: tuple[int, int] = (i, start_char_found)
        if end_char_found != -1:
            end_pos: tuple[int, int] = (i, end_char_found)
    
    heightmap[start_pos[0]] = heightmap[start_pos[0]].replace(start_char, 'a')
    heightmap[end_pos[0]] = heightmap[end_pos[0]].replace(end_char, 'z')

    return heightmap, start_pos, end_pos


def build_graph(heightmap: list[str]) -> dict[tuple[int, int], set[tuple[int, int]]]:
    graph = {}
    map_size = (len(heightmap), len(heightmap[0]))

    for i, line in enumerate(heightmap):
        for j in range(len(line)):
            current_pos = (i, j)
            connex = get_connex(current_pos, map_size)
            connex -= filter_steep(heightmap, current_pos, connex)

            graph[current_pos] = connex
    
    return graph


def build_graph2(
    heightmap: list[str], 
    start_pos: tuple[int, int], 
    end_pos: tuple[int, int]) -> dict[tuple[int, int], set[tuple[int, int]]]:

    graph = {}
    frontier = {start_pos}
    map_size = (len(heightmap), len(heightmap[0]))

    while frontier and end_pos not in graph.keys():
        new_frontier = set()

        for f in frontier:
            connex = get_connex(f, map_size)
            connex -= filter_steep(heightmap, f, connex)
            connex -= graph.keys()
            connex -= frontier

            new_frontier |= connex
            graph[f] = connex
        
        frontier = new_frontier
    
    return graph


def filter_steep(
    heightmap: list[str], 
    frontier: tuple[int, int], 
    connex: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Verify slope of pivot position and adjacent,
    returns steep adjacent positions to be filtered
    """

    filter_connex = set()
    frontier_val = ord(heightmap[frontier[0]][frontier[1]])

    for c in connex:
        connex_val = ord(heightmap[c[0]][c[1]])

        if abs(frontier_val - connex_val) > 1:
            filter_connex.add(c)
    
    return filter_connex


def get_connex(
    pos: set[int, int], 
    map_size: list[str]) -> set[tuple[int, int]]:
    """
    Returns adjacent positions from a pivot position by parameter
    """

    connex = set()

    if pos[0] > 0: connex.add((pos[0] - 1, pos[1])) # North
    if pos[0] < map_size[0] - 1: connex.add((pos[0] + 1, pos[1])) # South
    if pos[1] < map_size[1] - 1: connex.add((pos[0], pos[1] + 1)) # East
    if pos[1] > 0: connex.add((pos[0], pos[1] - 1)) # West

    return connex


def dfs(
    graph: dict[tuple[int, int], set[tuple[int, int]]], 
    start_pos: tuple[int, int], 
    end_pos: tuple[int, int], 
    visited: set[tuple[int, int]] = set()) -> int:
    """
    Traverse recursively the graph with depth first search method
    returns the lowest depth to find
    """

    if start_pos == end_pos:
        return len(visited)

    min_depth = math.inf
    visited.add(start_pos)
    frontier = graph[start_pos] - visited

    for f in frontier:
        frontier_depth = dfs(graph, f, end_pos, visited)
        min_depth = min(min_depth, frontier_depth)

    return min_depth


if __name__ == '__main__':
    heightmap = read_file()
    heightmap, start_pos, end_pos = get_pos(heightmap)
    # graph = build_graph(heightmap)
    graph = build_graph2(heightmap, start_pos, end_pos)
    min_depth = dfs(graph, (20, 73), end_pos)

    print('\nPoint 1')
    print('Fewest amount of steps: {0}'.format(min_depth))

    print('\nPoint 2')