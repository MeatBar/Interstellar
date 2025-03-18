from typing import List, Tuple

import networkx as nx

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate


def grid_to_pos(i, j):
    """
    TODO: WRITE THIS
    """
    return x, y


def weight_function(u: Coordinate, v: Coordinate) -> float:
    """
    Weight function for the edges of the graph
    :param u: source node
    :param v: target node
    :return: weight of the edge
    """
    if u.field_type == 1 or v.field_type == 1 or u.field_type == 2 or u.field_type == 2:
        return float('inf')
    return u.distance_to(v)


def grid_to_graph(grid: List[List[int]], sample_size: int) -> nx.Graph:
    """
    Converts a grid to a graph
    :param grid: 0 if empty, 1 if asteroid, 2 if black hole
    :return: graph with nodes named (x, y)
    """
    graph = nx.Graph()
    node_count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            graph.add_node(Coordinate(i, j))
            node_count += 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                continue
            u = None
            v = None
            # TODO: if running time is a problem, could maybe cut this by half by only doing right and down
            if i > 0 and grid[i - 1][j] == 0:
                u = Coordinate(*grid_to_pos(i, j), grid[i][j])
                v = Coordinate(*grid_to_pos(i - 1, j), grid[i - 1][j])
            if j > 0 and grid[i][j - 1] == 0:
                u = Coordinate(*grid_to_pos(i, j), grid[i][j])
                v = Coordinate(*grid_to_pos(i, j-1), grid[i][j-1])
            if i < len(grid) - 1 and grid[i + 1][j] == 0:
                u = Coordinate(*grid_to_pos(i, j), grid[i][j])
                v = Coordinate(*grid_to_pos(i+1, j), grid[i + 1][j])
            if j < len(grid[0]) - 1 and grid[i][j + 1] == 0:
                u = Coordinate(*grid_to_pos(i, j), grid[i][j])
                v = Coordinate(*grid_to_pos(i, j+1), grid[i][j+1])
            if u and v:
                graph.add_edge(u, v, weight=weight_function(u, v))
    return graph


def calculate_path(source: Coordinate, target: Coordinate, enemies: List[Enemy]) -> Tuple[List[Coordinate], nx.Graph]:
    """Calculates a path from source to target without any detection

    Note: The path must start at the source coordinate and end at the target coordinate!

    :param source: source coordinate of the spaceship
    :param target: target coordinate of the spaceship
    :param enemies: list of enemies along the way
    :return: list of calculated pathway points and the graph constructed
    """

    # Your objective is to write an algorithm that considering all of the above threats will generate the shortest
    # possible path you can calculate from source to target.
    #
    # Note that to be accepted, the returned path must not be detected by the bandits at any point!

    return [source, target], nx.Graph()
