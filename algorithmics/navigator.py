from typing import List, Tuple

import networkx as nx

from enemy.enemy import Enemy
from enemy.black_hole import BlackHole
from enemy.asteroids_zone import AsteroidsZone

from utils.coordinate import Coordinate

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
    
#limited blackhole support
def make_grid(enemies: List[Enemy], sample_size :int = 8) -> nx.Graph:
    """Creates a graph from the list of enemies

    :param enemies: list of enemies
    :return: graph constructed
    """
    graph = nx.Graph()
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
            normal_coordinates.append(coordinate * (sample_size / max_coordinate))
    
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

if __name__ == '__main__':
    #test enemy
    AsteroidsZone(Coordinate(0,0), 1)
    
    grid = make_grid([])
    print(grid)