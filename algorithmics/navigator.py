from typing import List, Tuple

import networkx as nx
import shapely as shp

from enemy.enemy import Enemy
from enemy.black_hole import BlackHole
from enemy.asteroids_zone import AsteroidsZone

from utils.coordinate import Coordinate

#todo : ADD 1 to each edge of grid to allow manuevering around obstacles

class Navigator:
    def calculate_rect_boundary(self) -> Tuple[Coordinate, Coordinate]:
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
    
    def calculate_boundries_and_stretch_factor(self) -> Tuple[Coordinate, Coordinate, int, int]:
        min_coordinate = rect[0]
        max_coordinate = rect[1]
        
        move_x = -min_coordinate.x
        move_y = -min_coordinate.y
        stretch_factor = sample_size/max(max_coordinate.x - min_coordinate.x, max_coordinate.y - min_coordinate.y)
        
        
    def normalize_coordinate(self) -> Coordinate:
        return Coordinate(round((coordinates.x + move_x) * stretch_factor), round((coordinates.y + move_y) * stretch_factor())) 

    #limited blackhole support
    def make_grid(enemies: List[Enemy], sample_size :int = 8) -> nx.Graph:
        """Creates a graph from the list of enemies

        :param enemies: list of enemies
        :return: graph constructed
        """
        min_coordinate, max_coordinate = Navigator.calculate_rect_boundary(enemies, Coordinate(0,0), Coordinate(10,10))
        
        astroids = [enemy for enemy in enemies if enemy.__class__.__name__ == 'AsteroidsZone']
        black_holes = [enemy for enemy in enemies if enemy.__class__.__name__ == 'BlackHole']
        
        grid = [[0]*sample_size] * sample_size
        
        #Uristic:
        # 0 - empty
        # 1 - astroid
        # 2 - blackhole
        # we divide all the coordinates by max_coordinate to get a value between 0 and 1
        # then we multiply by sample_size to get a value between 0 and sample_size
        polygons = []
        for astroid in astroids:
            normal_coordinates = []
            for coordinate in astroid.boundary:
                normal_coordinates.append(Navigator.normalize_coordinate(coordinate, min_coordinate, max_coordinate, sample_size))

            polygons.append(shp.Polygon(normal_coordinates))
        
        for x in range(sample_size):
            for y in range(sample_size):
                for polygon in polygons:
                    if polygon.contains(shp.Point(x, y)):
                        grid[x][y] = 1
        
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
    Coordinates = [Coordinate(0,0), Coordinate(0,1), Coordinate(1,1), Coordinate(1,0)]
    AsteroidsZone(Coordinates)
    
    grid = Navigator.make_grid([])
    print(grid)