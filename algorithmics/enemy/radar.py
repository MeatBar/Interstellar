import math
import random
from typing import List, Tuple

from shapely.geometry import Point, LineString

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
from algorithmics.utils.edge import Edge


class Radar(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a radar object at the location with the given detection radius

        :param center: location of the radar
        :param radius: detection radius of the radar
        """
        self.center = center
        self.radius = radius

        self.circle = Point(self.center.x, self.center.y).buffer(self.radius)

    def approximate_boundary(self, n: int = 30) -> List[Coordinate]:
        """Compute polygon approximating the boundary of the post

        The returned polygon will out-bound the circle

        :param n: number of vertices in the approximating polygon
        :return: polygon approximating the circle
        """

        angle_step = math.radians(360 / n)
        buffed_radius = self.radius / math.cos(angle_step / 2)
        return [Coordinate(self.center.x + buffed_radius * math.sin(i * angle_step),
                           self.center.y + buffed_radius * math.cos(i * angle_step))
                for i in range(n)]

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

    def detection(self, start: Coordinate, end: Coordinate) -> float:

        radar_intersection = LineString([[start.x, start.y], [end.x, end.y]]).intersection(self.circle)
        if radar_intersection.length == 0:
            return 0

        start = Coordinate(radar_intersection.coords[0][0], radar_intersection.coords[0][1])
        end = Coordinate(radar_intersection.coords[1][0], radar_intersection.coords[1][1])
        edge = Edge(start, end)

        projection = edge.project_coordinate(self.center)
        distance_from_edge = edge.distance_to_point(self.center)

        legal_leg = Edge(projection.shifted(distance_from_edge, edge.direction + math.pi),
                         projection.shifted(distance_from_edge, edge.direction))
        legal_part = edge.intersect_with_interlacing_edge(legal_leg)
        legal_length = 0 if legal_part is None else legal_part.length
        return start.distance_to(end) - legal_length

    def detected_segments(self, start: Coordinate, end: Coordinate) -> List[Tuple[Coordinate, Coordinate]]:
        radar_intersection = LineString([[start.x, start.y], [end.x, end.y]]).intersection(self.circle)
        if radar_intersection.length == 0:
            return []

        start = Coordinate(radar_intersection.coords[0][0], radar_intersection.coords[0][1])
        end = Coordinate(radar_intersection.coords[1][0], radar_intersection.coords[1][1])
        edge = Edge(start, end)

        projection = edge.project_coordinate(self.center)
        distance_from_edge = edge.distance_to_point(self.center)

        legal_leg = Edge(projection.shifted(distance_from_edge, edge.direction + math.pi),
                         projection.shifted(distance_from_edge, edge.direction))
        legal_part = edge.intersect_with_interlacing_edge(legal_leg)

        if legal_part is None:
            return [(start, end)]

        if abs(edge.direction - legal_part.direction) > 1e-2:
            legal_part = legal_part.reversed

        detected_segments = []
        if edge.start != legal_part.start:
            detected_segments.append((edge.start, legal_part.start))
        if legal_part.end != edge.end:
            detected_segments.append((legal_part.end, edge.end))
        return detected_segments

    def sample(self) -> Coordinate:
        """Sample a random coordinate uniformly in the radar's area

        :return: coordinate chosen randomly in uniform distribution in the radar's area
        """

        radius = math.sqrt(random.random()) * self.radius
        theta = random.uniform(0, 2 * math.pi)
        return self.center + Coordinate(math.cos(theta), math.sin(theta)) * radius
