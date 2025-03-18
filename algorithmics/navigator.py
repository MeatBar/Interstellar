from typing import List, Tuple

import networkx as nx

from enemy.enemy import Enemy
from enemy.black_hole import BlackHole
from enemy.asteroids_zone import AsteroidsZone

from utils.coordinate import Coordinate


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

#todo : ADD 1 to each edge of grid to allow manuevering around obstacles

class Navigator:

    def calculate_rect_boundary(enemies: List[Enemy], source: Coordinate, target: Coordinate) -> Tuple[Coordinate, Coordinate]:
        """Calculates the boundary of the rectangle that contains all the objects

        return a tuple with the minimum and maximum coordinates of the rectangle
        """
        min_coordinate = Coordinate(min(source.x, target.x), min(source.y, target.y))
        max_coordinate = Coordinate(max(source.x, target.x), max(source.y, target.y))

        astroids = [enemy for enemy in enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in enemies if enemy.__class__.__name__ == 'BlackHole']

        for astroid in astroids:
            for coordinate in astroid.boundary:
                if coordinate.x < min_coordinate.x:
                    min_coordinate.x = coordinate.x
                if coordinate.y < min_coordinate.y:
                    min_coordinate.y = coordinate.y
                if coordinate.x > max_coordinate.x:
                    max_coordinate.x = coordinate.x
                if coordinate.y > max_coordinate.y:
                    max_coordinate.y = coordinate.y

        for black_hole in black_holes:
            if black_hole.center.x - black_hole.radius < min_coordinate.x:
                min_coordinate.x = black_hole.center.x - black_hole.radius
            if black_hole.center.y - black_hole.radius < min_coordinate.y:
                min_coordinate.y = black_hole.center.y - black_hole.radius
            if black_hole.center.x + black_hole.radius > max_coordinate.x:
                max_coordinate.x = black_hole.center.x + black_hole.radius
            if black_hole.center.y + black_hole.radius > max_coordinate.y:
                max_coordinate.y = black_hole.center.y + black_hole.radius

        return min_coordinate, max_coordinate

    def normalize_coordinate(coordinates: Coordinate, min_coordinate: Coordinate, max_coordinate: Coordinate, sample_size: int) -> Coordinate:
        move_x = min(min_coordinate.x, 0)
        move_y = min(min_coordinate.y, 0)
        max_coordinate = max(max_coordinate.x, max_coordinate.y)

        stretch_factor = sample_size/max_coordinate
        return Coordinate(round((coordinates.x + move_x) * stretch_factor), round((coordinates.y + move_y) * stretch_factor()))

    #limited blackhole support
    def make_grid(enemies: List[Enemy], sample_size :int = 8) -> nx.Graph:
        """Creates a graph from the list of enemies

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

        :param enemies: list of enemies
        :return: graph constructed
        """
        min_coordinate, max_coordinate = calculate_rect_boundary(enemies, Coordinate(0,0), Coordinate(10,10))

        astroids = [enemy for enemy in enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in enemies if enemy.__class__.__name__ == 'BlackHole']

        grid = [[0]*sample_size] * sample_size

        #Uristic:
        # 0 - empty
        # 1 - astroid
        # 2 - blackhole
        # we divide all the coordinates by max_coordinate to get a value between 0 and 1
        # then we multiply by sample_size to get a value between 0 and sample_size
        for astroid in astroids:
            normal_coordinates = []
            for coordinate in astroid.boundary:
                normal_coordinates.append(normalize_coordinate(coordinate, min_coordinate, max_coordinate, sample_size))

        return grid


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
