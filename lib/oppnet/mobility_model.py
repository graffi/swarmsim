import random
from enum import Enum

from ..std_lib import NE, E, SE, SW, W, NW


class Mode(Enum):
    """
    Used to easily distinguish MobilityModels.
    """
    Random_Walk = 0
    Back_And_Forth = 1
    Circle = 2
    Random = 3
    Static = 4
    Zonal = 5
    Random_Mode = 6


class MobilityModel:
    """
    Class to define particle movement.
    """

    @staticmethod
    def get(particle):
        """
        Returns the mobility_model attribute of a :param particle:
        :param particle: the particle to check
        :return: the mobility_model attribute
        """
        return getattr(particle, "mobility_model")

    def __init__(self, start_x, start_y, mode: Mode, length=(5, 30), zone=(), starting_dir=None):
        """
        Constructor.
        :param start_x: starting x coordinate
        :param start_y: starting y coordinate
        :param mode: the Mode of the MobilityModel
        :param length: the length of a route as interval, e.g. for Random_Walk
        :param zone: the zone as square with 4 values: top-left x, top-left y, bottom-right x, bottom-right y
        :param starting_dir: initial direction
        """
        if mode == Mode.Random_Mode:
            mode = random.choice(list(Mode)[:-1])
        if mode == Mode.Zonal:
            self.min_x = zone[0]
            self.min_y = zone[1]
            self.max_x = zone[2]
            self.max_y = zone[3]
        else:
            self.min_x = start_x - length[1]
            self.min_y = start_y - length[1]
            self.max_x = start_x + length[1]
            self.max_y = start_y + length[1]
        self.mode = mode
        self.steps = 0
        self.min_length = length[0]
        self.max_length = length[1]
        if not starting_dir:
            self.starting_dir = self.random_direction()
        else:
            self.starting_dir = starting_dir
        self.route_length = random.randint(self.min_length, self.max_length)
        self.return_dir = self.__return_direction()
        self.current_dir = self.starting_dir

    def set(self, particle):
        """
        Sets the mobility_model attribute of :param particle:.
        :param particle: the particle the MobilityModel as attribute to.
        """
        setattr(particle, "mobility_model", self)

    def __return_direction(self):
        """
        Calculates the return direction based on starting direction, i.e. the opposing direction.
        :return: the opposing direction to starting_dir
        """
        return self.starting_dir - 3 if self.starting_dir > 2 else self.starting_dir + 3
    
    def next_direction(self, current_x_y=None):
        """
        Determines the next direction of the model.
        :param current_x_y: the current x and y coordinates of the particle as tuple
        :return: the next direction
        """
        if self.mode == Mode.Back_And_Forth:
            return self.__back_and_forth__()
        elif self.mode == Mode.Random_Walk:
            return self.__random_walk__()
        elif self.mode == Mode.Circle:
            return self.__circle__()
        elif self.mode == Mode.Random:
            return self.__random__()
        elif self.mode == Mode.Static:
            return False
        elif self.mode == Mode.Zonal:
            return self.__zonal__(current_x_y)

    def __random__(self):
        """
        The next direction in random mode.
        :return: next direction
        """
        self.current_dir = MobilityModel.random_direction()
        return self.current_dir

    def __circle__(self):
        """
        The next direction in circle mode.
        :return: next direction
        """
        if self.steps < self.route_length:
            self.steps += 1
        else:
            if self.current_dir == NE:
                self.current_dir = NW
            elif self.current_dir == NW:
                self.current_dir = W
            elif self.current_dir == W:
                self.current_dir = SW
            elif self.current_dir == SW:
                self.current_dir = SE
            elif self.current_dir == SE:
                self.current_dir = E
            elif self.current_dir == E:
                self.current_dir = NE
            self.steps = 1
            # new circle if we walked a full circle
            if self.current_dir == self.starting_dir:
                self.route_length = random.randint(1, self.max_length)
                self.starting_dir = MobilityModel.random_direction()
                self.current_dir = self.starting_dir
        return self.current_dir

    def __random_walk__(self):
        """
        The next direction in random walk mode.
        :return: next direction
        """
        if self.steps < self.route_length:
            self.steps += 1
            return self.current_dir
        else:
            self.steps = 1
            self.route_length = random.randint(1, self.max_length)
            return self.__random__()

    def __back_and_forth__(self):
        """
        The next direction in back and forth mode.
        :return: next direction
        """
        if 0 <= self.steps < self.route_length:
            self.steps += 1
            return self.starting_dir
        elif self.steps == self.route_length:
            self.steps = -1
            return self.return_dir
        elif self.steps == -self.route_length:
            self.steps = 1
            return self.starting_dir
        else:
            self.steps -= 1
            return self.return_dir

    def __zonal__(self, current_x_y):
        """
        The next direction in zonal mode.
        :return: next direction
        """
        (x, y) = current_x_y
        # check if at min_x then head anywhere but west

        directions = {W,
                      SW,
                      NW,
                      E,
                      SE,
                      NE}

        if self.min_x >= x:
            directions = directions.difference({W, SW, NW})
        if self.max_x <= x:
            directions = directions.difference({E, SE, NE})
        if self.min_y >= y:
            directions = directions.difference({SE, SW})
        if self.max_y <= y:
            directions = directions.difference({NE, NW})

        next_dir = MobilityModel.random_direction(list(directions))
        return next_dir

    @staticmethod
    def random_direction(directions=None):
        """
        A random direction from list :param directions:.
        :param directions: a list of directions.
        :return: a random next direction in directions, or complete random
        """
        if directions is None:
            directions = [W, SW, NW, E, SE, NE]
        return random.choice(directions)
