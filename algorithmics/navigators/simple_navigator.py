import math
from typing import List

import networkx as nx

from algorithmics.enemy.radar import Radar
from algorithmics.navigators.navigator import Navigator
from algorithmics.utils.coordinate import Coordinate


class SimpleNavigator(Navigator):
    """Navigator that deals with single-target in a no-detection case"""
    def __init__(self, enemies):
        self.enemies = enemies
        self.radars = [enemy for enemy in enemies if isinstance(enemy, Radar)]
        self.total_danger = 0


    def legal_radar_edge(self, edge):
        a, b = edge[0], edge[1]
        return all([radar.is_legal_leg(a,b) for radar in self.radars])

    def path_length(self, path):
        length = 0
        for i in range(1, len(path)):
            length += path[i].distance_to(path[i-1])
        return length


    def create_big_graph(self, graph: nx.DiGraph, max_detection: float):
        # create intercontinental edges list
        new_edge_list = []
        for edge in graph.edges:
            if not self.legal_radar_edge(edge):
                new_edge_list.append((edge[0], edge[1]))
        # create big graph (Coordinate(x,y), depth)
        big_graph = nx.DiGraph()
        for depth in range(int(max_detection)):
            for node in graph.nodes:
                big_graph.add_node((node.x, node.y, depth))
            for edge in graph.edges:
                if self.legal_radar_edge(edge):
                    u, v = edge[0], edge[1]
                    big_graph.add_edge((u.x, u.y, depth), (v.x, v.y, depth), dist=u.distance_to(v))
        print("Duplicated graph")
        # add new edges to big graph
        for depth in range(int(max_detection)):
            for edge in new_edge_list:
                u, v = edge[0], edge[1]
                distance = u.distance_to(v)
                if depth + math.ceil(distance) < int(max_detection):
                    big_graph.add_edge((u.x, u.y, depth), (v.x, v.y, depth + math.ceil(distance)), dist=distance)
        print("Connected the duplicates")
        return big_graph

    def compute_path(self, graph: nx.DiGraph, source: Coordinate, targets: List[Coordinate], max_detection: float) -> \
            List[Coordinate]:
        big_graph = self.create_big_graph(graph)
        target_list = []
        path_list = []
        for i in range(len(target_list)-1):
            target_paths = []
            for detection in range(int(max_detection)):
                path = nx.shortest_path(big_graph, (target_list[i].x, target_list[i].y, 0), (target_list[i+1].x, target_list[i+1].y, detection), weight='dist')
                path = [Coordinate(node[0], node[1]) for node in path]
                print(f"Found best path {detection}/{max_detection}")
                length = self.path_length(path)
                target_paths.append((path, length, detection))
            path_list.append(target_paths)

        return

    def assert_input_legality(self, targets: List[Coordinate], max_detection: float) -> None:
        # # if len(targets) == 1 and max_detection == 0:
        #     return
        return
        # raise ValueError(f'Illegal input for {type(self)}')
