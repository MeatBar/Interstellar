import networkx as nx
from tqdm import tqdm

from algorithmics.extenders.exntender import Extender
from algorithmics.utils.coordinate import Coordinate


class PRMExtender(Extender):
    SAMPLES = 2000
    EDGE_RADIUS = 5

    def extend(self, graph: nx.DiGraph) -> None:

        print('Extending graph inside radars')

        if len(self.environment.radars) == 0:
            return

        # Sample nodes randomly in the radars' area
        new_nodes = []
        samples_per_radar = self.SAMPLES // len(self.environment.radars)
        for radar in self.environment.radars:
            new_nodes += [radar.sample() for _ in range(samples_per_radar)]

        # Iteratively add the nodes to the graph
        for node in tqdm(new_nodes):
            self._connect_new_node(graph, node)

    def _connect_new_node(self, graph: nx.DiGraph, node: Coordinate) -> None:
        """Connects a new node to the graph in a PRM logic

        :param graph: graph to be extended
        :param node: node to be added
        :return: None
        """

        # Add node to the graph
        graph.add_node(node)
        for other in graph.nodes:

            # Skip current node and nodes further than EDGE_RADIUS from it
            if other == node or node.distance_to(other) > self.EDGE_RADIUS:
                continue

            self._connect_nodes(graph, node, other)
