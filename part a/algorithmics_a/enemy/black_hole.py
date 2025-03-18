from algorithmics_b.enemy.enemy import Enemy
from algorithmics_b.utils.coordinate import Coordinate


class BlackHole(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a new observation post object anchored at the given point

        :param center: the location of the observation post
        :param radius: observation distance of the post
        """
        self.center = center
        self.radius = radius
