from typing import Optional, List

from algorithmics.utils.coordinate import Coordinate


class Edge:

    def __init__(self, start: Coordinate, end: Coordinate):
        self.start = start
        self.end = end

    @property
    def length(self) -> float:
        return self.start.distance_to(self.end)

    @property
    def direction(self) -> float:
        return self.start.direction_to(self.end)

    @property
    def reversed(self) -> 'Edge':
        return Edge(self.end, self.start)

    @property
    def vector(self) -> Coordinate:
        return self.end - self.start

    @property
    def midpoint(self) -> Coordinate:
        return Coordinate((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    @property
    def endpoints(self) -> List[Coordinate]:
        return [self.start, self.end]

    def project_coordinate(self, c: Coordinate) -> Coordinate:
        vector_from_start = c - self.start
        projection_distance_from_start = self.vector.dot(vector_from_start) / self.length
        return self.start.shifted(projection_distance_from_start, self.direction)

    def distance_to_point(self, c: Coordinate) -> float:
        vector_from_start = c - self.start
        return abs(self.vector.cross(vector_from_start) / self.length)

    def intersect_with_interlacing_edge(self, other: 'Edge') -> Optional['Edge']:

        if all(my_endpoint.x <= other_endpoint.x for other_endpoint in other.endpoints
               for my_endpoint in self.endpoints):
            return None

        if all(my_endpoint.x >= other_endpoint.x for other_endpoint in other.endpoints
               for my_endpoint in self.endpoints):
            return None

        all_endpoints = self.endpoints + other.endpoints
        all_endpoints = sorted(all_endpoints, key=lambda p: p.x)
        return Edge(all_endpoints[1], all_endpoints[2])
