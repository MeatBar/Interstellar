from typing import List, Tuple

import networkx
import networkx as nx

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate


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

def get_closest_point_on_graph(target_coord,sample_size,min_x,max_x,min_y,max_y):
    normalized_coord = Navigator.normalize_coordinate(target_coord)

    normalized_coord.x = round(normalized_coord.x)
    normalized_coord.y = round(normalized_coord.y)

    return Navigator.invertNormalization(normalized_coord)


def translate_edgelist_to_path(edge_list: List[Tuple[Coordinate]]) -> List[Coordinate]:
    return [edge[0] for edge in edge_list] + [edge_list[-1][1]]

def dist(a, b):
    return a.distance_to(b)
def get_edgelist_from_graph(G,source,target,sample_size,min_x,max_x,min_y,max_y):
    source_on_graph = get_closest_point_on_graph(source,sample_size,min_x,max_x,min_y,max_y)
    target_on_graph = get_closest_point_on_graph(target,sample_size,min_x,max_x,min_y,max_y)

    path = networkx.astar_path(G,source_on_graph,target_on_graph,heuristic=dist,weight='weight')
    return path