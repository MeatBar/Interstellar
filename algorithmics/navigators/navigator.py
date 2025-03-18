from abc import ABC, abstractmethod
from typing import List

import networkx as nx

from algorithmics.utils.coordinate import Coordinate


class Navigator(ABC):

    def navigate(self, graph: nx.DiGraph, source: Coordinate, targets: List[Coordinate], max_detection: float) -> \
            List[Coordinate]:
        """Find path in the graph

        :param graph: graph to be searched
        :param source: source of the path
        :param targets: visit-required targets of the path
        :param max_detection: maximal allowed detection in path
        :return: computed path
        """

        # self.assert_input_legality(targets, max_detection)

        try:
            print('Computing path')
            path = self.compute_path(graph, source, targets, max_detection)
        # If not path exists, return an empty path
        except nx.NetworkXNoPath:
            path = []

        print('Returning path')
        return path

    def get_dist(self, G, source, target):
        path = nx.shortest_path(G, source, target, weight='dist')
        length = 0
        for i in range(1, len(path)):
            length += path[i].distance_to(path[i - 1])
        return length

    @abstractmethod
    def compute_path(self, graph: nx.DiGraph, source: Coordinate, targets: List[Coordinate], max_detection: float) -> \
            List[Coordinate]:
        """Perform the path search algorithm

        :param graph: graph to be searched
        :param source: source of the path
        :param targets: visit-required targets of the path
        :param max_detection: maximal allowed detection in path
        :return: computed path
        """
        tsp = nx.approximation.traveling_salesman_problem(graph, targets + [source], weight='dist', cycle=True)
        i = tsp.index(source)
        tsp = tsp[i:] + tsp[:i]

        if self.get_dist(graph,source, tsp[1]) < self.get_dist(graph,source, tsp[-1]):
            return tsp
        else:
            tsp = tsp[::-1]
            tsp.pop()
            tsp = [source] + tsp
        return tsp

    @abstractmethod
    def assert_input_legality(self, targets: List[Coordinate], max_detection: float) -> None:
        """Verify that the input matches assumptions of the navigator

        :param targets: visit-required targets of the path
        :param max_detection: maximal allowed detection in path
        :return: None
        :raise: ValueError, if input doesn't match the navigator assumptions
        """
        pass
