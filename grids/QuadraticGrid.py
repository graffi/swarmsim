from grids.Grid import Grid


class QuadraticGrid(Grid):

    def __init__(self, size):
        super().__init__()
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def directions(self):
        return {"LEFT": (-1, 0, 0),
                "RIGHT": (1, 0, 0),
                "UP": (0, 1, 0),
                "DOWN": (0, -1, 0)}

    def get_box(self, width):
        locations = []
        for x in range(int(-width / 2), int(width / 2)):
            for y in range(int(-width / 2), int(width / 2)):
                locations.append((x, y, 0.0))
        return locations

    def is_valid_location(self, location):
        if location[0] % 1 == 0 and location[1] % 1 == 0:
            return True
        else:
            return False

    def get_nearest_location(self, coordinates):
        return (round(coordinates[0]),
                round(coordinates[1]), 0.0)

    def get_dimension_count(self):
        return 2

    def get_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def get_center(self):
        return 0, 0, 0
