from itertools import combinations
from typing import List

import networkx as nx

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.environment import Environment
from algorithmics.enemy.radar import Radar
from algorithmics.extenders.exntender import Extender
from algorithmics.utils.coordinate import Coordinate


class OutlineExtender(Extender):

    def __init__(self, environment: Environment, source: Coordinate, targets: List[Coordinate]):
        self.source = source
        self.targets = targets
        self.radius_scale = 50 # Maximum radius in the problem
        super().__init__(environment)

    def get_enemies_outlines(self) -> List[Coordinate]:
        """Create list of coordinates defining enemies outline

        :return: None
        """

        coordinates = []

        # For every enemy, add nodes to the graph
        for enemy in self.environment.enemies:

            # If the enemy is an asteroid zone, add its corners
            if isinstance(enemy, AsteroidsZone):
                coordinates.extend(enemy.boundary)

            # If the enemy is an observation post, add its approximation
            if isinstance(enemy, BlackHole) or isinstance(enemy, Radar):
                self.radius_scale = max(enemy.radius, self.radius_scale)
                coordinates.extend(enemy.approximate_boundary())

        return coordinates

    def get_radar_grids(self, r_steps: int = 10, n: int = 20) -> List[Coordinate]:
        """Create list of coordinates representing the grids inside the radar

        :return: The grids
        """
        coordinates = []
        for enemy in self.environment.enemies:
            if isinstance(enemy, Radar):
                coordinates.extend(enemy.radar_grid(r_steps, n))

        return coordinates

    def extend(self, graph: nx.DiGraph) -> None:

        print('Initializing graph')

        coordinates = [self.source] + self.targets + self.get_enemies_outlines() + self.get_radar_grids(20, 20)
        graph.add_nodes_from(coordinates)
        print("Got nodes")
        for start, end in combinations(coordinates, 2):
            if start.distance_to(end) < self.radius_scale / 2:
                self._connect_nodes(graph, start, end)

