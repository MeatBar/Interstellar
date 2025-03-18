from typing import List, Tuple

import networkx as nx
import shapely as shp
import shapely.geometry

from enemy.enemy import Enemy
from enemy.black_hole import BlackHole
from enemy.asteroids_zone import AsteroidsZone

from utils.coordinate import Coordinate


#todo : ADD 1 to each edge of grid to allow manuevering around obstacles

class Navigator:

    def __init__(self, enemies: List[Enemy], source: Coordinate, target: Coordinate, sample_size: int):
        self.enemies = enemies
        self.source = source
        self.target = target
        self.sample_size = sample_size
        
        
        min_coordinate, max_coordinate = self.calculate_rect_boundary()      
        self.min_coordinate = min_coordinate
        self.max_coordinate = max_coordinate
  
        #Need to call calculate_stretch_factor_and_move to update these values
        self.stretch_factor = 1
        self.move_x = 0
        self.move_y = 0
        self.calc_stretch_factor_and_move() #Update those values
        
        #Update in the future when algorithm runs
        self.grid = None 
        self.graph = None
        
    def calculate_rect_boundary(self) -> Tuple[Coordinate, Coordinate]:
        """Calculates the boundary of the rectangle that contains all the objects

        return a tuple with the minimum and maximum coordinates of the rectangle
        """
        min_coordinate = Coordinate(min(self.source.x, self.target.x), min(self.source.y, self.target.y))
        max_coordinate = Coordinate(max(self.source.x, self.target.x), max(self.source.y, self.target.y))

        astroids = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'BlackHole']

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

        min_coordinate.x -= 1
        min_coordinate.y -= 1
        max_coordinate.x += 1
        max_coordinate.y += 1
        return min_coordinate, max_coordinate

    def calc_stretch_factor_and_move(self) -> None:
        self.move_x = -self.min_coordinate.x
        self.move_y = -self.min_coordinate.y
        self.stretch_factor = self.sample_size/max(self.max_coordinate.x - self.min_coordinate.x, self.max_coordinate.y - self.min_coordinate.y)
        
        
    def weight_function(self, u: Coordinate, v: Coordinate) -> float:
        """
        Weight function for the edges of the graph
        :param u: source node
        :param v: target node
        :return: weight of the edge
        """
        if u.field_type == 1 or v.field_type == 1 or u.field_type == 2 or u.field_type == 2:
            return float('inf')
        line = shapely.geometry.LineString([[u.x,u.y], [v.x,v.y]])
        astroids = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'BlackHole']
        for astroid in astroids:
            polygon = shapely.geometry.Polygon(astroid.boundary)
            if shp.intersects(polygon, line):
                return float('inf')
        return u.distance_to(v)

    def normalize_coordinate(self, coordinates: Coordinate) -> Coordinate:
        x = round((coordinates.x + self.move_x) * self.stretch_factor)
        y = round((coordinates.y + self.move_y) * self.stretch_factor)
        return Coordinate(x, y)

    def grid_to_pos(self, i, j):
        x = (i / self.stretch_factor) - self.move_x
        y = (j / self.stretch_factor) - self.move_y
        return Coordinate(x, y)

    def make_grid(self) -> List[List[int]]:
        """Creates a graph from the list of enemies, limited blackhole support
            :param enemies: list of enemies
            :return: graph constructed
        """
        min_coordinate, max_coordinate = self.calculate_rect_boundary()

        astroids = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in self.enemies if enemy.__class__.__name__ == 'BlackHole']

        grid = [[0] * self.sample_size] * self.sample_size

        # Uristic:
        # 0 - empty
        # 1 - astroid
        # 2 - blackhole
        # we divide all the coordinates by max_coordinate to get a value between 0 and 1
        # then we multiply by sample_size to get a value between 0 and sample_size
        for astroid in astroids:
            normal_coordinates = []
            for coordinate in astroid.boundary:
                normal_coordinates.append(self.normalize_coordinate(coordinate))

        return grid


    def grid_to_graph(self, grid: List[List[int]]) -> nx.Graph:
        """
        Converts a grid to a graph
        :param grid: 0 if empty, 1 if asteroid, 2 if black hole
        :return: graph with nodes named (x, y)
        """
        graph = nx.Graph()
        node_count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x, y = self.grid_to_pos(i, j).pos()
                graph.add_node(Coordinate(x, y, grid[i][j]))
                node_count += 1
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # TODO: if running time is a problem, could maybe cut this by half by only doing right and down
                u = Coordinate(*self.grid_to_pos(i, j).pos(), grid[i][j])
                if i > 0:
                    v = Coordinate(*self.grid_to_pos(i - 1, j).pos(), grid[i - 1][j])
                    graph.add_edge(u, v, weight=self.weight_function(u, v))
                if j > 0:
                    v = Coordinate(*self.grid_to_pos(i, j-1).pos(), grid[i][j-1])
                    graph.add_edge(u, v, weight=self.weight_function(u, v))
                if i < len(grid) - 1:
                    v = Coordinate(*self.grid_to_pos(i+1, j).pos(), grid[i + 1][j])
                    graph.add_edge(u, v, weight=self.weight_function(u, v))
                if j < len(grid[0]) - 1:
                    v = Coordinate(*self.grid_to_pos(i, j+1).pos(), grid[i][j+1])
                    graph.add_edge(u, v, weight=self.weight_function(u, v))
        return graph

    def get_closest_point_on_graph(self, coord):
        normalized_coord = self.normalize_coordinate(coord)

        normalized_coord.x = round(normalized_coord.x)
        normalized_coord.y = round(normalized_coord.y)

        return self.grid_to_pos(normalized_coord.x, normalized_coord.y)

    def translate_edgelist_to_path(self, edge_list: List[Coordinate]) -> List[Coordinate]:
        return [edge for edge in edge_list] + [edge_list[-1]]


    def get_edgelist_from_graph(self, G):
        source_on_graph = self.get_closest_point_on_graph(self.source)
        target_on_graph = self.get_closest_point_on_graph(self.target)

        path = nx.astar_path(G, source_on_graph, target_on_graph, weight='weight')
        return path

    def get_solution(self):
        grid = self.make_grid()
        graph = self.grid_to_graph(grid)
        edge_list = self.get_edgelist_from_graph(graph)
        solution = self.translate_edgelist_to_path(edge_list)
        return [self.source, *solution, self.target]


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
    nav = Navigator(enemies, source, target, 200)
    solution = nav.get_solution()
    return solution, nx.Graph()
