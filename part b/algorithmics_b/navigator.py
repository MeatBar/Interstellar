from typing import List, Tuple

import networkx as nx

from algorithmics_b.enemy.enemy import Enemy
from algorithmics_b.enemy.environment import Environment
from algorithmics_b.extenders.outline_extender import OutlineExtender
from algorithmics_b.navigators.simple_navigator import SimpleNavigator
from algorithmics_b.utils.coordinate import Coordinate


# Navigator

def get_length(path):
    length = 0
    for i in range(1, len(path)):
        length += path[i].distance_to(path[i-1])
    return length


def calculate_path(source: Coordinate, targets: List[Coordinate], enemies: List[Enemy], allowed_detection: float = 0) -> Tuple[List[Coordinate], nx.Graph]:
    """Calculates a path from source to target without any detection

    Note: The path must start at the source coordinate and end at the target coordinate!

    :param source: source coordinate of the spaceship
    :param targets: target coordinate of the spaceship
    :param enemies: list of enemies along the way
    :param allowed_detection: maximum allowed distance of radar detection
    :return: list of calculated path waypoints and the graph constructed
    """

    graph = nx.DiGraph()
    env = Environment(enemies)

    OutlineExtender(env, source, targets).extend(graph)

    path = SimpleNavigator().navigate(graph, source, targets, allowed_detection)
    print("L:", get_length(path))
    return path, graph
