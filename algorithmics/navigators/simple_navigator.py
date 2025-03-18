from typing import List

import networkx as nx

from algorithmics.navigators.navigator import Navigator
from algorithmics.utils.coordinate import Coordinate


class SimpleNavigator(Navigator):
    """Navigator that deals with single-target in a no-detection case"""

    def get_dist(self,graph,source,target):
        path = nx.shortest_path(graph, source, target, weight='dist')
        length = 0
        for i in range(1, len(path)):
            length += path[i].distance_to(path[i - 1])
        return length

    def compute_path(self, graph: nx.DiGraph, source: Coordinate, targets: List[Coordinate], max_detection: float) -> \
            List[Coordinate]:
        # #return nx.shortest_path(graph, source, targets[0], weight='dist')
        # print(graph)
        # targs = targets + [source]
        # print(targs)
        # tsp = nx.approximation.traveling_salesman_problem(G=graph,weight='weight',nodes=targs,cycle=False)
        # print(tsp)
        # return tsp
        # i = tsp.index(source)
        # tsp = tsp[i:]+tsp[:i]
        #
        # if self.get_dist(graph,source,tsp[1]) < self.get_dist(graph,source,tsp[-1]):
        #     return tsp
        # else:
        #     tsp = tsp[::-1]
        #     tsp.pop()
        #     tsp = [source]+tsp
        # print(tsp)
        # return tsp
        targs = targets #+[source]
        super_graph = nx.Graph()
        super_graph.add_nodes_from(targs)
        for i in range(len(targs)):
            for j in range(i,len(targs)):
                dist = self.get_dist(graph,targs[i],targs[j])
                super_graph.add_edge(targs[i],targs[j],dist=dist)
        tsp = nx.approximation.christofides(super_graph, weight="dist")

        min_dist = float('inf')
        min_target = None
        for target in targets:
            dist = self.get_dist(graph,source,target)
            if dist < min_dist:
                min_dist = dist
                min_target = target
        i = tsp.index(min_target)
        tsp = tsp[i:]+tsp[:i]

        if self.get_dist(graph,min_target,tsp[1]) < self.get_dist(graph,min_target,tsp[-1]):
            return tsp
        else:
            tsp = tsp[::-1]
            tsp.pop()
            tsp = [source]+tsp
        tsp = [source]+tsp
        path = []
        for u,v in [(tsp[i],tsp[i+1]) for i in range(len(tsp)-1)]:
            path = path + nx.shortest_path(graph,u,v,weight='dist')

        return path











    def assert_input_legality(self, targets: List[Coordinate], max_detection: float) -> None:
        if len(targets) == 1 and max_detection == 0:
            return

        raise ValueError(f'Illegal input for {type(self)}')
