import math
from typing import List
import numpy as np

from shapely.geometry import Point, LineString

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate


class Radar(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a radar object at the location with the given detection radius

        :param center: location of the radar
        :param radius: detection radius of the radar
        """
        self.center = center
        self.radius = radius

        self.circle = Point(self.center.x, self.center.y).buffer(self.radius)

    @staticmethod
    def _compute_direction_diff(direction1: float, direction2: float):
        angle_diff = (direction1 - direction2) % (2 * math.pi)
        if angle_diff <= math.pi / 2:
            return angle_diff
        if angle_diff <= math.pi:
            return math.pi - angle_diff
        if angle_diff <= 3 * math.pi / 2:
            return angle_diff - math.pi
        return 2 * math.pi - angle_diff

    def is_legal_leg(self, start: Coordinate, end: Coordinate) -> bool:
        """Checks if the leg [start, end] is a legal leg in the radar.

        :param start: the start coordinate of the leg
        :param end: the end coordinate of the leg
        :return: True if the leg is legal and False otherwise.
        """
        radar_intersection = LineString([[start.x, start.y], [end.x, end.y]]).intersection(self.circle)
        if radar_intersection.length == 0:
            return True

        start = Coordinate(radar_intersection.coords[0][0], radar_intersection.coords[0][1])
        end = Coordinate(radar_intersection.coords[1][0], radar_intersection.coords[1][1])
        movement_direction = start.direction_to(end)
        for p in [start, end]:
            if self._compute_direction_diff(movement_direction, p.direction_to(self.center)) < math.radians(45):
                return False
        return True

    def approximate_boundary(self, n: int = 20) -> List[Coordinate]:
        """Compute polygon approximating the boundary of the post

        The returned polygon will out-bound the circle

        :param n: number of vertices in the approximation polygon
        :return: polygon approximating the circle
        """

        angle_step = math.radians(360 / n)
        buffed_radius = self.radius / math.cos(angle_step / 2)
        return [Coordinate(self.center.x + buffed_radius * math.sin(i * angle_step),
                           self.center.y + buffed_radius * math.cos(i * angle_step))
                for i in range(n)]

    def radar_grid(self, r_steps: int = 10, n: int = 20):
        """Compute a grid of points inside of the radar radius
        :param dr: resolution of radial steps in the grid
        :param n: number of steps to cover in the angular direction
        """
        radius_space = np.linspace(0,1, r_steps)
        radius_space = radius_space * radius_space * radius_space * self.radius

        total_grid = []

        for radius in radius_space:
            fake_radar = Radar(self.center, radius)
            total_grid += fake_radar.approximate_boundary(n)
        return total_grid